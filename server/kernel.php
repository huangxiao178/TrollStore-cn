<?php
/*
 * Kernelcache resolver for 巨魔苹果玩家 mobile installer.
 * Compatible with the server's PHP 5.4 runtime.
 * The endpoint never accepts an arbitrary URL: it only selects an active
 * Apple firmware link returned by AppleDB for the requested device/build and
 * rewrites it to the local range-capable Nginx proxy.
 */
error_reporting(0);
header('Content-Type: application/json; charset=utf-8');

function kernel_json($ok, $msg, $extra = array()) {
    $data = array_merge(array('ok' => $ok, 'msg' => $msg), $extra);
    die(json_encode($data, JSON_UNESCAPED_UNICODE));
}

$os = isset($_GET['os']) ? $_GET['os'] : 'iOS';
$build = isset($_GET['build']) ? $_GET['build'] : '';
$model = isset($_GET['model']) ? $_GET['model'] : '';

if (!preg_match('/^(iOS|iPadOS)$/', $os) ||
    !preg_match('/^[0-9A-Za-z.]+$/', $build) ||
    !preg_match('/^i[A-Za-z0-9,]+$/', $model)) {
    kernel_json(false, '设备固件参数无效');
}

$apiUrl = 'https://api.appledb.dev/' . rawurlencode(strtolower($os)) . '/' .
          rawurlencode($os . ';' . $build) . '.json';
$ch = curl_init($apiUrl);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
curl_setopt($ch, CURLOPT_TIMEOUT, 20);
curl_setopt($ch, CURLOPT_USERAGENT, 'JumoKernelResolver/1.0');
$body = curl_exec($ch);
$curlError = curl_error($ch);
$httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($body === false || $httpCode !== 200) {
    kernel_json(false, '无法查询设备固件（HTTP ' . $httpCode . '）');
}

$firmware = json_decode($body, true);
if (!is_array($firmware) || !isset($firmware['sources']) || !is_array($firmware['sources'])) {
    kernel_json(false, '固件查询结果无效');
}

foreach ($firmware['sources'] as $source) {
    if (!is_array($source) || !isset($source['type']) ||
        !in_array($source['type'], array('ota', 'ipsw'), true)) {
        continue;
    }
    if (!isset($source['deviceMap']) || !is_array($source['deviceMap']) ||
        !in_array($model, $source['deviceMap'], true)) {
        continue;
    }
    if ($source['type'] === 'ota' && isset($source['prerequisiteBuild']) &&
        $source['prerequisiteBuild']) {
        continue;
    }
    if (!isset($source['links']) || !is_array($source['links'])) {
        continue;
    }

    foreach ($source['links'] as $link) {
        if (!is_array($link) || empty($link['url']) ||
            (isset($link['active']) && !$link['active'])) {
            continue;
        }
        $parts = parse_url($link['url']);
        if (!$parts || empty($parts['host']) || empty($parts['path'])) {
            continue;
        }
        // Only proxy Apple's public CDN. No open-proxy behavior.
        if (!in_array(strtolower($parts['host']), array(
            'updates.cdn-apple.com', 'updates-http.cdn-apple.com'
        ), true)) {
            continue;
        }

        $proxyUrl = 'http://124.223.199.167/kernel-proxy' . $parts['path'];
        kernel_json(true, 'ok', array(
            'url' => $proxyUrl,
            'isOTA' => $source['type'] === 'ota',
            'build' => $build,
            'model' => $model
        ));
    }
}

kernel_json(false, '没有找到该设备对应的固件');
?>
