<?php

use Illuminate\Http\Request;
use Illuminate\Contracts\Debug\ExceptionHandler;
use NourApi\Framework\Exceptions\Handler;
use NourApi\Framework\Application;

$app = new Application;
$app->configure('app');
$app->singleton(ExceptionHandler::class, Handler::class);

$app->middleware(static function ($request, $next) {
    $response = $next($request);
    $response->headers->set('X-Application', 'Nour-API');
    return $response;
});

$app->router->get('/health', ['as' => 'health', static fn () => ['status' => 'ok']]);
$app->router->get('/users/{id:[0-9]+}', static fn ($id) => ['id' => $id]);
$app->router->post('/users', static function (Request $request) {
    $data = app('validator')->make($request->all(), ['email' => 'required|email'])->validate();
    return response()->json($data, 201);
});

return $app;
