/* global api */
class jpcn_Youdao {
    constructor(options) {
        this.options = options;
        this.maxexample = 2;
        this.word = '';
    }

    async displayName() {
        let locale = await api.locale();
        if (locale.indexOf('jp') != -1) return 'moji日语词典';
        if (locale.indexOf('jp') != -1) return 'moji日语词典';
        return 'moji Dictionary';
    }

    setOptions(options) {
        this.options = options;
        this.maxexample = options.maxexample;
    }

    async findTerm(word) {
        this.word = word;
        return await this.findYoudao(word);
    }

    async findYoudao(word) {
        if (!word) return null;

        let base = 'https://api.mojidict.com/parse/functions/union-api';
        let url = base + encodeURIComponent(word);
        let doc = '';
        try {
            let data = await fetch("https://api.mojidict.com/parse/functions/union-api", {
                "headers": {
                    "accept": "*/*",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "content-type": "text/plain",
                    "sec-ch-ua": "\"Microsoft Edge\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site"
                },
                "referrer": "https://www.mojidict.com/",
                "referrerPolicy": "strict-origin-when-cross-origin",
                "body": "{\"functions\":[{\"name\":\"search-all\",\"params\":{\"text\":\"こわが\",\"types\":[102,106,103]}},{\"name\":\"mojitest-examV2-searchQuestion-v2\",\"params\":{\"text\":\"こわが\",\"limit\":1,\"page\":1}},{\"name\":\"deconjugateWithKeyWord\",\"params\":{\"text\":\"こわが\"}}],\"_SessionToken\":\"r:603e6e9430f3c668ad0ffc93730a8dff\",\"_ClientVersion\":\"js3.4.1\",\"_ApplicationId\":\"E62VyFVLMiW7kvbtVq3p\",\"g_os\":\"PCWeb\",\"g_ver\":\"v4.7.7.20240327\",\"_InstallationId\":\"ce0e63fe-d00a-4079-9576-545cd648eca6\"}",
                "method": "POST",
                "mode": "cors",
                "credentials": "omit"
            });
            let parser = new DOMParser();
            doc = parser.parseFromString(data, 'text/xml');
        } catch (err) {
            return null;
        }
        console.log(doc);
        return definition;
    }

    async findYoudaoOld(word) {
        if (!word) return null;

        let base = 'https://dict.youdao.com/fsearch?client=deskdict&keyfrom=chrome.extension&pos=-1&doctype=xml&xmlVersion=3.2&dogVersion=1.0&vendor=unknown&appVer=3.1.17.4208&le=fr&q=';
        let url = base + encodeURIComponent(word);
        let doc = '';
        try {
            let data = await api.fetch(url);
            let parser = new DOMParser();
            doc = parser.parseFromString(data, 'text/xml');
        } catch (err) {
            return null;
        }

        let xmlroot = doc.getElementsByTagName('yodaodict')[0];
        let trans = xmlroot.getElementsByTagName('translation');
        let definition = '';
        if (!trans[0] || !trans[0].childNodes[0])
            return null;

        for (let i = 0; i < trans.length; i++) {
            definition += trans[i].getElementsByTagName('content')[0].childNodes[0].nodeValue + '<br>';
        }
        return definition;
    }

}


