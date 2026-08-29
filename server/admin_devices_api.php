<?php
/**
 * Device view for the admin console (PHP 5.4 / MySQL compatible).
 *
 * This endpoint only reads bound-device status and changes the numeric
 * license state (1 active, 2 frozen).  It never uninstalls TrollStore or
 * deletes applications from a phone.
 */
if (file_exists('/etc/secure-install/db.php')) {
    require '/etc/secure-install/db.php';
} else {
    $db_host = getenv('TROLL_DB_HOST');
    $db_port = intval(getenv('TROLL_DB_PORT'));
    $db_user = getenv('TROLL_DB_USER');
    $db_pass = getenv('TROLL_DB_PASSWORD');
    $db_name = getenv('TROLL_DB_NAME');
    if (!$db_host) $db_host = 'localhost';
    if (!$db_port) $db_port = 3306;
}

$db_tbl = 'troll_codes';
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, no-cache, must-revalidate');

$secure_cookie = !empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off';
session_name('troll_admin');
session_set_cookie_params(0, '/', '', $secure_cookie, true);
session_start();

function device_json($payload, $status) {
    http_response_code($status);
    die(json_encode($payload, JSON_UNESCAPED_UNICODE));
}
function device_ok($payload) {
    $payload['ok'] = true;
    device_json($payload, 200);
}
function device_fail($message, $status) {
    device_json(array('ok' => false, 'msg' => $message), $status);
}
function device_hash_equals($known, $user) {
    if (function_exists('hash_equals')) return hash_equals($known, $user);
    if (!is_string($known) || !is_string($user) || strlen($known) !== strlen($user)) return false;
    $diff = 0;
    for ($i = 0; $i < strlen($known); $i++) $diff |= ord($known[$i]) ^ ord($user[$i]);
    return $diff === 0;
}
function device_csrf() {
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = function_exists('openssl_random_pseudo_bytes')
            ? bin2hex(openssl_random_pseudo_bytes(24))
            : sha1(uniqid(mt_rand(), true));
    }
    return $_SESSION['csrf'];
}
function device_require($write) {
    if (empty($_SESSION['admin_authenticated'])) device_fail('请先登录后台', 401);
    if ($write) {
        $provided = isset($_SERVER['HTTP_X_CSRF_TOKEN']) ? $_SERVER['HTTP_X_CSRF_TOKEN'] : '';
        if (!$provided || !device_hash_equals(device_csrf(), $provided)) {
            device_fail('会话已失效，请刷新页面后重试', 419);
        }
    }
}
function device_db() {
    global $db_host, $db_port, $db_user, $db_pass, $db_name;
    $db = new mysqli($db_host, $db_user, $db_pass, $db_name, $db_port);
    if ($db->connect_error) device_fail('数据库连接失败', 503);
    $db->set_charset('utf8mb4');
    return $db;
}
function device_bind($stmt, $types, $params) {
    $refs = array($types);
    foreach ($params as $i => $value) $refs[] = &$params[$i];
    return call_user_func_array(array($stmt, 'bind_param'), $refs);
}
function device_rows($stmt) {
    if (!$stmt->execute()) device_fail('数据库查询失败', 500);
    $stmt->store_result();
    $meta = $stmt->result_metadata();
    if (!$meta) return array();
    $fields = array();
    $row = array();
    while ($field = $meta->fetch_field()) $fields[] = &$row[$field->name];
    call_user_func_array(array($stmt, 'bind_result'), $fields);
    $rows = array();
    while ($stmt->fetch()) {
        $item = array();
        foreach ($row as $key => $value) $item[$key] = $value;
        $rows[] = $item;
    }
    return $rows;
}
function device_label($status) {
    $status = intval($status);
    if ($status === 2) return '已冻结';
    return '正常';
}

$action = isset($_GET['action']) ? $_GET['action'] : '';
if ($action === 'me') {
    if (empty($_SESSION['admin_authenticated'])) device_json(array('ok' => false), 401);
    device_ok(array('csrf' => device_csrf()));
}

device_require($action === 'status');
$db = device_db();

if ($action === 'summary') {
    $summary = array('total' => 0, 'active' => 0, 'frozen' => 0);
    $result = $db->query("SELECT COUNT(DISTINCT udid) AS total,
        COUNT(DISTINCT CASE WHEN status = 1 THEN udid END) AS active,
        COUNT(DISTINCT CASE WHEN status = 2 THEN udid END) AS frozen
        FROM $db_tbl WHERE udid <> '' AND status IN (1, 2)");
    if ($result) {
        $row = $result->fetch_assoc();
        $summary['total'] = intval($row['total']);
        $summary['active'] = intval($row['active']);
        $summary['frozen'] = intval($row['frozen']);
    }
    device_ok(array('summary' => $summary));
}

if ($action === 'list') {
    $page = max(1, intval(isset($_POST['page']) ? $_POST['page'] : 1));
    $page_size = max(10, min(100, intval(isset($_POST['page_size']) ? $_POST['page_size'] : 20)));
    $search = isset($_POST['search']) ? trim($_POST['search']) : '';
    $where = array("udid <> ''", 'status IN (1, 2)');
    $params = array();
    $types = '';
    if ($search !== '') {
        $where[] = '(code LIKE ? OR udid LIKE ? OR device_model LIKE ? OR ios_version LIKE ?)';
        $needle = '%' . $search . '%';
        $params[] = $needle; $params[] = $needle; $params[] = $needle; $params[] = $needle;
        $types .= 'ssss';
    }
    $condition = implode(' AND ', $where);

    $countStmt = $db->prepare("SELECT COUNT(*) AS n FROM $db_tbl WHERE $condition");
    if ($types !== '') device_bind($countStmt, $types, $params);
    $countRows = device_rows($countStmt);
    $total = $countRows ? intval($countRows[0]['n']) : 0;

    $offset = ($page - 1) * $page_size;
    $listStmt = $db->prepare("SELECT code, udid, status, device_model, ios_version,
        ts_version, activated_at, install_status, install_time, last_status
        FROM $db_tbl WHERE $condition
        ORDER BY COALESCE(install_time, activated_at) DESC LIMIT ? OFFSET ?");
    $listParams = $params;
    $listParams[] = $page_size;
    $listParams[] = $offset;
    device_bind($listStmt, $types . 'ii', $listParams);
    $rows = device_rows($listStmt);
    foreach ($rows as $index => $row) {
        $rows[$index]['status_label'] = device_label($row['status']);
        $rows[$index]['last_active'] = $row['install_time'] ? $row['install_time'] : $row['activated_at'];
    }
    device_ok(array('rows' => $rows, 'total' => $total, 'page' => $page, 'page_size' => $page_size));
}

if ($action === 'status') {
    $code = trim(isset($_POST['code']) ? $_POST['code'] : '');
    $operation = isset($_POST['operation']) ? $_POST['operation'] : '';
    if ($code === '' || !in_array($operation, array('freeze', 'unfreeze'), true)) device_fail('参数无效', 400);
    $find = $db->prepare("SELECT udid, status FROM $db_tbl WHERE code = ? LIMIT 1");
    $find->bind_param('s', $code);
    $found = device_rows($find);
    if (!$found) device_fail('未找到对应卡密', 404);
    if (trim($found[0]['udid']) === '') device_fail('该卡密尚未绑定设备', 409);
    $next = $operation === 'freeze' ? 2 : 1;
    $update = $db->prepare("UPDATE $db_tbl SET status = ? WHERE code = ? AND udid <> ''");
    $update->bind_param('is', $next, $code);
    if (!$update->execute()) device_fail('状态更新失败', 500);
    device_ok(array('status' => $next, 'status_label' => device_label($next)));
}

device_fail('unknown action', 404);
?>
