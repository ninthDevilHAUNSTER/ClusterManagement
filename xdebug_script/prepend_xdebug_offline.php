<?php 
// 增加命令行传参脚本
error_reporting(E_ERROR);
ini_set('error_reporting', E_ERROR);
date_default_timezone_set("Asia/Shanghai");
// 在触发到特定行的时候，把相应的变量输出出来
ini_set("xdebug.collect_params", 4);
ini_set("xdebug.remote_log", "xdebug.log");
ini_set("xdebug.dump_globals", "on");
ini_set("xdebug.dump.REQUEST", "*");
ini_set("xdebug.dump.COOKIE", "*");
ini_set("xdebug.dump.SERVER", "REQUEST_URI,REQUEST_METHOD");

// script

// xdebug_start_code_coverage(XDEBUG_CC_UNUSED | XDEBUG_CC_DEAD_CODE); 当统计文件行的时候，开启该选项。
xdebug_start_code_coverage();
function shutdown_ashd9va()
{
    // Registering shutdown function inside shutdown function
    // is a trick to make this function be called last!
    register_shutdown_function('shutdown_kdnw92j');
    error_log('registering second shutdown function' . $_SERVER["SCRIPT_FILENAME"]);
}

function shutdown_kdnw92j()
{
    error_log('calling end coverage (shutdown)' . $_SERVER["SCRIPT_FILENAME"]);
    end_coverage_cav39s8hca(True);
}

function end_coverage_cav39s8hca($caller_shutdown_func = False)
{
//     error_log(implode(',', $_COOKIE));
    error_log('stopping coverage (' . xdebug_code_coverage_started() . ') ' . $_SERVER["SCRIPT_FILENAME"]);
    $current_dir = __DIR__;
    $test_name = (isset($_COOKIE['test_name']) && !empty($_COOKIE['test_name'])) ? htmlspecialchars($_COOKIE['test_name'], ENT_QUOTES, 'UTF-8') : 'unknown_test_' . time();
    $fk_software_id = (isset($_COOKIE['software_id']) && !empty($_COOKIE['software_id'])) ? intval($_COOKIE['software_id']) : -1;
    $fk_software_version_id = (isset($_COOKIE['software_version_id']) && !empty($_COOKIE['software_version_id'])) ? intval($_COOKIE['software_version_id']) : -1;
    $test_group = (isset($_COOKIE['test_group']) && !empty($_COOKIE['test_group'])) ? htmlspecialchars($_COOKIE['test_group'], ENT_QUOTES, 'UTF-8') : 'default';
    if ($test_group == 'default') {
        return True;
    }
    $dt = new DateTime("now", new DateTimeZone("Asia/Shanghai"));
//    $coverageName = $current_dir . '/coverages/coverage-' . $test_name . '-' . $dt->format('m-d-Y_Hi');
    $coverageName = $current_dir . '/coverages/coverage-' . $test_name . '-' . $dt->format('d-H-i-s');
    //                                                                                      d-H-i-s
    // 29-04-38-23 =>
    // D:\wamp\xdebug_scripts/coverages/coverage-piwigo283_robercrwaler-
    // Y-m-d H:i:s
    $_request_hash = sha1($coverageName);
    $_new_path_detection_flag = True;
    try {
        $codecoverageData = json_encode(xdebug_get_code_coverage());
        if ($caller_shutdown_func) {
            error_log('calling xdebug stop');
            xdebug_stop_code_coverage(); // true to destroy in memory information, not resuming later
        }
//        file_put_contents($coverageName . '.json', $codecoverageData);
        $included_files = get_included_files();
        $_new_path_detection_flag = ensure_new_path($coverageName, $test_group, $codecoverageData, $included_files, $fk_software_id, $fk_software_version_id);
        if ($_new_path_detection_flag) {
            write_to_db_vb76bvgbasc($coverageName, $test_group, $codecoverageData, $included_files, $fk_software_id, $fk_software_version_id, $_request_hash);
        }
    } catch (Exception $ex) {
        error_log($ex);
        file_put_contents($coverageName . '.ex', $ex);
    }
    //echo "<input type='hidden' id='_REQUEST_HASH_dfnajszKOFHN' value='$_request_hash'/>";
    //echo "<input type='hidden' id='_NEW_PATH_DETECTION_dfnajszKOFHN' value='$_new_path_detection_flag'/>";
}


function ensure_new_path($coverageName, $test_group, $codecoverageData, $included_files, $fk_software_id, $fk_software_version_id)
{
    # return if detect new path.
    $mysqli = new mysqli("cc", "admin", "admin123", "code_coverage", 3306);
    $mysqli->autocommit(FALSE);
    if (mysqli_connect_errno()) {
        error_log(sprintf("Connect failed: %s", mysqli_connect_error()));
        exit();
    }
    return True;
}

function write_to_db_vb76bvgbasc($coverageName, $test_group, $codecoverageData, $included_files, $fk_software_id, $fk_software_version_id, $_request_hash)
{
    $mysqli = new mysqli("cc", "admin", "admin123", "code_coverage", 3306);
    $mysqli->autocommit(FALSE);
    if (mysqli_connect_errno()) {
        error_log(sprintf("Connect failed: %s", mysqli_connect_error()));
        exit();
    }
    // Create test entry
    $test_id = 0;
    if ($stmt = $mysqli->prepare('INSERT INTO tests (test_name, test_group, test_date, fk_software_id, fk_software_version_id, request_hash,test_data) VALUES (?,?,?,?,?,?,?) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)')) {
        $date = date("Y-m-d H:i:s");
        $data_collection = _data_collection();
        $stmt->bind_param("sssiiss", $coverageName, $test_group, $date, $fk_software_id, $fk_software_version_id, $_request_hash, serialize($data_collection));
        $res = $stmt->execute();
        $test_id = mysqli_insert_id($mysqli);
    } else
        error_log($mysqli->error);
    $file_id = 0;
    // bulk insert all
    $str_line_coverage = '';
    foreach (json_decode($codecoverageData) as $filename => $values) { // Iterate over each covered file
        if ($stmt = $mysqli->prepare('INSERT INTO covered_files (file_name, fk_test_id) VALUES (?,?) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)')) {
            $stmt->bind_param("si", $filename, $test_id);
            $stmt->execute(); // Insert covered files into the database
            $file_id = mysqli_insert_id($mysqli);
        } else
            error_log($mysqli->error);
        foreach ($values as $line_no => $status) { // Iterate over each covered line
            if ($str_line_coverage !== '') {
                $str_line_coverage = $str_line_coverage . ', ';
            }
            $str_line_coverage = $str_line_coverage . sprintf('(%s,%s,%s)', $line_no, $status, $file_id);
        }
    }
    // Bulk insert covered lines into the database
    if ($stmt = $mysqli->prepare('INSERT IGNORE INTO covered_lines (line_number, run, fk_file_id) VALUES ' . $str_line_coverage)) {
        $stmt->execute();
    } else
        error_log($mysqli->error);
    foreach ($included_files as $filename) {
        if ($stmt = $mysqli->prepare('INSERT INTO included_files (file_name, fk_test_id) VALUES (?,?)')) {
            $stmt->bind_param("si", $filename, $test_id);
            $stmt->execute();
        } else
            error_log($mysqli->error);
    }
    $mysqli->commit();
    # 返回一个标识符，用来标记
}

function _data_collection()
{
    // ini_set("xdebug.dump.REQUEST", "*");
// ini_set("xdebug.dump.COOKIE", "*");
// ini_set("xdebug.dump.SERVER", "REQUEST_URI,REQUEST_METHOD");
    $r = array();
    $tmp_cookie = $_COOKIE;
    $tmp_cookie = array_diff_key($tmp_cookie, array(
        'test_name' => 0,
        'test_group' => 0,
        'software_id' => 0,
        'software_version_id' => 0,
        'XDEBUG_SESSION' => 0,
    )); # delete meaningless items;
    $r[] = array('REQUEST_URI' => $_SERVER['REQUEST_URI'], 'REQUEST_METHOD' => $_SERVER['REQUEST_METHOD']);
    $r[] = $_POST;
    $r[] = $_GET;
    $r[] = $tmp_cookie;
    return $r;
}


register_shutdown_function('shutdown_ashd9va');
error_log('registered shutdown_ashd9va as shutdown function');

?>
