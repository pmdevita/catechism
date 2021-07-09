function get(url) {
    let p = new Promise(function (resolve, reject) {
        fetch(url)
            .then(r => r.json())
            .then(r => {resolve(r)})
    });
    return p;
}

function getText(start, end) {
    if (end == undefined || end == null) {
        return get(`/text/${start}`);
    } else {
        return get(`/text/${start}/${end}`);
    }
}

export {getText};