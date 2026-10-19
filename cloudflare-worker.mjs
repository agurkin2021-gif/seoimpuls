export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.hostname === 'www.seoimpuls.com') {
      url.hostname = 'seoimpuls.com';
      url.protocol = 'https:';
      return Response.redirect(url.toString(), 301);
    }

    return env.ASSETS.fetch(request);
  }
};
