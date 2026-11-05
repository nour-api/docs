<?php

$autoload = $argv[1] ?? __DIR__.'/../../framework/vendor/autoload.php';
require $autoload;
$app = require __DIR__.'/../examples/application.php';
$app['config']->set('app.debug', false);
$app->configure('logging');
$app['config']->set('logging.default', 'null');
$cases = [
    ['/health', 'GET', [], 200, ['status' => 'ok']],
    ['/users/42', 'GET', [], 200, ['id' => '42']],
    ['/users', 'POST', ['email' => 'dev@example.com'], 201, ['email' => 'dev@example.com']],
    ['/users', 'POST', ['email' => 'invalid'], 422, null],
    ['/users/no-number', 'GET', [], 404, null],
    ['/health', 'POST', [], 405, null],
    ['/health', 'HEAD', [], 200, null],
];
try {
    foreach ($cases as [$uri, $method, $data, $status, $body]) {
        $response = $app->handle(NourApi\Framework\Http\Request::create($uri, $method, $data, [], [], ['HTTP_ACCEPT' => 'application/json']));
        if ($response->getStatusCode() !== $status || ($body !== null && json_decode($response->getContent(), true) !== $body)
            || $response->headers->get('X-Application') !== 'Nour-API' || ($method === 'HEAD' && $response->getContent() !== '')) {
            throw new RuntimeException("Documentation example failed: {$method} {$uri}");
        }
    }
    echo 'PASS: '.count($cases)." executable documentation scenarios\n";
} catch (Throwable $e) {
    fwrite(STDERR, $e->getMessage()."\n");
    exit(1);
}
