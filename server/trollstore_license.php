<?php
/**
 * Mobile TrollStore license heartbeat (PHP 5.4 compatible).
 *
 * This endpoint is separate from the legacy admin/remote API. It performs a
 * status decision plus a last-seen update only; it never uninstalls TrollStore,
 * removes files, or changes device state.
 */
error_reporting(0);
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    die(json_encode(array('ok' => false, 'status' => 'invalid_request')));
}

$code = isset($_POST['code']) ? trim($_POST['code']) : '';
$udid = isset($_POST['udid']) ? trim($_POST['udid']) : '';
$ts   = isset($_POST['ts']) ? intval($_POST['ts']) : 0;

if ($code === '' || strlen($code) > 32 || $udid === '' || strlen($udid) > 128) {
    die(json_encode(array('ok' => false, 'status' => 'invalid_request')));
}

// Reject stale requests so a captured request cannot be replayed forever.
if ($ts <= 0 || abs(time() - $ts) > 600) {
    die(json_encode(array('ok' => false, 'status' => 'stale_request')));
}

// Keep database credentials outside the web root.  The production server
// supplies /etc/secure-install/db.php; environment variables are supported
// for a staging server so this file never needs a password in source control.
if (file_exists('/etc/secure-install/db.php')) {
    require '/etc/secure-install/db.php';
} else {
    $db_host = getenv('TROLL_DB_HOST') ? getenv('TROLL_DB_HOST') : 'localhost';
    $db_port = intval(getenv('TROLL_DB_PORT'));
    $db_user = getenv('TROLL_DB_USER');
    $db_pass = getenv('TROLL_DB_PASSWORD');
    $db_name = getenv('TROLL_DB_NAME');
    if (!$db_port) $db_port = 3306;
}
if (!$db_user || !$db_name) {
    die(json_encode(array('ok' => false, 'status' => 'server_error')));
}
$db = new mysqli($db_host, $db_user, $db_pass, $db_name, $db_port);
if ($db->connect_error) {
    die(json_encode(array('ok' => false, 'status' => 'server_error')));
}
$db->set_charset('utf8mb4');

$stmt = $db->prepare('SELECT status, udid, expires_at FROM troll_codes WHERE code = ? LIMIT 1');
if (!$stmt) {
    die(json_encode(array('ok' => false, 'status' => 'server_error')));
}
$stmt->bind_param('s', $code);
$stmt->execute();
$stmt->store_result();
$stmt->bind_result($status, $boundUdid, $expiresAt);
if (!$stmt->fetch()) {
    $stmt->close();
    die(json_encode(array('ok' => false, 'status' => 'unbound')));
}
$stmt->close();

$status = intval($status);
if ($status === 2) {
    die(json_encode(array('ok' => false, 'status' => 'frozen')));
}
if ($status !== 1 || strcasecmp($boundUdid, $udid) !== 0) {
    die(json_encode(array('ok' => false, 'status' => 'unbound')));
}
if ($expiresAt !== null && $expiresAt !== '' && strtotime($expiresAt) < time()) {
    die(json_encode(array('ok' => false, 'status' => 'expired')));
}

// Record that the installed TrollStore app checked in. The numeric status
// fields match the live schema: status 1=active, install_status 1=installed.
$report = $db->prepare('UPDATE troll_codes SET last_status = ?, install_status = 1, install_time = NOW() WHERE code = ? AND udid = ? AND status = 1');
if ($report) {
    $lastStatus = 'active';
    $report->bind_param('sss', $lastStatus, $code, $udid);
    $report->execute();
    $report->close();
}

die(json_encode(array('ok' => true, 'status' => 'active', 'expires_at' => $expiresAt)));
?>
