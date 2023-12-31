bodyDefault = b'''
importScripts('worker-testharness.js');
importScripts('test-helpers.sub.js');
importScripts('/common/get-host-info.sub.js');

var host_info = get_host_info();

test(function() {
    var import_script_failed = false;
    try {
      importScripts(host_info.HTTPS_REMOTE_ORIGIN +
        base_path() + 'empty.js');
    } catch(e) {
      import_script_failed = true;
    }
    assert_true(import_script_failed,
                'Importing the other origins script should fail.');
  }, 'importScripts test for default-src');

test(function() {
    assert_throws_js(EvalError,
                     function() { eval('1 + 1'); },
                     'eval() should throw EvalError.')
    assert_throws_js(EvalError,
                     function() { new Function('1 + 1'); },
                     'new Function() should throw EvalError.')
  }, 'eval test for default-src');

async_test(function(t) {
    fetch(host_info.HTTPS_REMOTE_ORIGIN +
          base_path() + 'fetch-access-control.py?ACAOrigin=*',
          {mode: 'cors'})
      .then(function(response){
          assert_unreached('fetch should fail.');
        }, function(){
          t.done();
        })
      .catch(unreached_rejection(t));
  }, 'Fetch test for default-src');

async_test(function(t) {
    var REDIRECT_URL = host_info.HTTPS_ORIGIN +
      base_path() + 'redirect.py?Redirect=';
    var OTHER_BASE_URL = host_info.HTTPS_REMOTE_ORIGIN +
      base_path() + 'fetch-access-control.py?'
    fetch(REDIRECT_URL + encodeURIComponent(OTHER_BASE_URL + 'ACAOrigin=*'),
          {mode: 'cors'})
      .then(function(response){
          assert_unreached('Redirected fetch should fail.');
        }, function(){
          t.done();
        })
      .catch(unreached_rejection(t));
  }, 'Redirected fetch test for default-src');'''

bodyScript = b'''
importScripts('worker-testharness.js');
importScripts('test-helpers.sub.js');
importScripts('/common/get-host-info.sub.js');

var host_info = get_host_info();

test(function() {
    var import_script_failed = false;
    try {
      importScripts(host_info.HTTPS_REMOTE_ORIGIN +
        base_path() + 'empty.js');
    } catch(e) {
      import_script_failed = true;
    }
    assert_true(import_script_failed,
                'Importing the other origins script should fail.');
  }, 'importScripts test for script-src');

test(function() {
    assert_throws_js(EvalError,
                     function() { eval('1 + 1'); },
                     'eval() should throw EvalError.')
    assert_throws_js(EvalError,
                     function() { new Function('1 + 1'); },
                     'new Function() should throw EvalError.')
  }, 'eval test for script-src');

async_test(function(t) {
    fetch(host_info.HTTPS_REMOTE_ORIGIN +
          base_path() + 'fetch-access-control.py?ACAOrigin=*',
          {mode: 'cors'})
      .then(function(response){
          t.done();
        }, function(){
          assert_unreached('fetch should not fail.');
        })
      .catch(unreached_rejection(t));
  }, 'Fetch test for script-src');

async_test(function(t) {
    var REDIRECT_URL = host_info.HTTPS_ORIGIN +
      base_path() + 'redirect.py?Redirect=';
    var OTHER_BASE_URL = host_info.HTTPS_REMOTE_ORIGIN +
      base_path() + 'fetch-access-control.py?'
    fetch(REDIRECT_URL + encodeURIComponent(OTHER_BASE_URL + 'ACAOrigin=*'),
          {mode: 'cors'})
      .then(function(response){
          t.done();
        }, function(){
          assert_unreached('Redirected fetch should not fail.');
        })
      .catch(unreached_rejection(t));
  }, 'Redirected fetch test for script-src');'''

bodyConnect = b'''
importScripts('worker-testharness.js');
importScripts('test-helpers.sub.js');
importScripts('/common/get-host-info.sub.js');

var host_info = get_host_info();

test(function() {
    var import_script_failed = false;
    try {
      importScripts(host_info.HTTPS_REMOTE_ORIGIN +
        base_path() + 'empty.js');
    } catch(e) {
      import_script_failed = true;
    }
    assert_false(import_script_failed,
                 'Importing the other origins script should not fail.');
  }, 'importScripts test for connect-src');

test(function() {
    var eval_failed = false;
    try {
      eval('1 + 1');
      new Function('1 + 1');
    } catch(e) {
      eval_failed = true;
    }
    assert_false(eval_failed,
                 'connect-src without unsafe-eval should not block eval().');
  }, 'eval test for connect-src');

async_test(function(t) {
    fetch(host_info.HTTPS_REMOTE_ORIGIN +
          base_path() + 'fetch-access-control.py?ACAOrigin=*',
          {mode: 'cors'})
      .then(function(response){
          assert_unreached('fetch should fail.');
        }, function(){
          t.done();
        })
      .catch(unreached_rejection(t));
  }, 'Fetch test for connect-src');

async_test(function(t) {
    var REDIRECT_URL = host_info.HTTPS_ORIGIN +
      base_path() + 'redirect.py?Redirect=';
    var OTHER_BASE_URL = host_info.HTTPS_REMOTE_ORIGIN +
      base_path() + 'fetch-access-control.py?'
    fetch(REDIRECT_URL + encodeURIComponent(OTHER_BASE_URL + 'ACAOrigin=*'),
          {mode: 'cors'})
      .then(function(response){
          assert_unreached('Redirected fetch should fail.');
        }, function(){
          t.done();
        })
      .catch(unreached_rejection(t));
  }, 'Redirected fetch test for connect-src');'''

def main(request, response):
    headers = [(b'Content-Type', b'application/javascript')]
    directive = request.GET[b'directive']
    body = b'ERROR: Unknown directive'
    if directive == b'connect':
        headers.append((b'Content-Security-Policy', b"connect-src 'self'"))
        body = bodyConnect
    elif directive == b'default':
        headers.append((b'Content-Security-Policy', b"default-src 'self'"))
        body = bodyDefault
    elif directive == b'script':
        headers.append((b'Content-Security-Policy', b"script-src 'self'"))
        body = bodyScript
    return headers, body
