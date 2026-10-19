export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.hostname === 'www.seoimpuls.com') {
      url.hostname = 'seoimpuls.com';
      url.protocol = 'https:';
      return Response.redirect(url.toString(), 301);
    }

    if (request.method !== 'GET') {
      return env.ASSETS.fetch(request);
    }

    const cache = caches.default;
    const cacheKey = new Request(url.toString(), request);
    const cached = await cache.match(cacheKey);
    if (cached) {
      return cached;
    }

    const response = await env.ASSETS.fetch(request);

    if (response.status !== 200) {
      return response;
    }

    const headers = new Headers(response.headers);
    headers.set('Cache-Control', 'public, max-age=7200');

    const cachedResponse = new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers
    });

    ctx.waitUntil(cache.put(cacheKey, cachedResponse.clone()));
    return cachedResponse;
  }
};
