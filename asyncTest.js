function getDataJSONP(url, callbackName = 'handleData') {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url, window.location.href);
        urlObj.searchParams.set('callback', callbackName);
        window[callbackName] = (data) => {
            resolve(data);
            delete window[callbackName];
            script.remove();
        };
        const script = document.createElement('script');
        script.src = urlObj.toString();
        script.onerror = reject;
        document.body.appendChild(script);
    });
}

(async () => {
    const data = await getDataJSONP(`http://localhost:8081/seismic.jsonp.php`);
    console.log(data);
})();