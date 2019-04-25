const { get } = require('http');
const { generate_cookie } = require('./get_generator.js');
const { writeFile } = require('fs');

const header = {
    'Host': 'www.thebeerstore.ca',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
},
cookie_path = 'cookie.json';

get('http://www.thebeerstore.ca/beers/search/', {'headers': header}, resp => {
    resp.setEncoding('utf8');
    let raw_data = '';

    resp.on('data', raw => { raw_data += raw; });
    resp.on('end', () => {
        const cookie = generate_cookie(raw_data);
        const tmp = { 'cookie': cookie };

        writeFile(cookie_path, JSON.stringify(tmp), e => {
            if(e) console.log(e);
            else console.log('Good write');
        });
    });
});
