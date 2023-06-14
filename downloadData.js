'use strict';

const { getToken, getData } = require('./utils');
const jsonfile = require('jsonfile');
const fs = require('fs');
const endpoints = require(`${__dirname}/endpoints/endpoints.${process.argv[2]}.json`)

const pageSizeDefault = 200;

const writeFile = (filename, page, endpoint) =>
  new Promise(async (resolve, reject) => {
    const { url } = endpoint;
    const { token_type, access_token } = (await getToken(endpoint)).data;

    try {
      const info = await getData(url, { pageSize: pageSizeDefault, page }, token_type, access_token);
      if (info.status === 200 && info.data.results && info.data.results.length > 0) {
        jsonfile.writeFile(filename, info.data.results, { spaces: 2 }, err => {
          if (err) {
            reject(err);
          }
        });

        resolve(info.data.pagination);
      }
      reject(info);
    } catch (err) {
      reject(err);
    }
  });

const download = async (page, dir, supplier_id, endpoint, pages) => {
  let filename = `data-${String(page).padStart(10, '0')}.json`;
  let realfilename = `${dir}/${filename}`;

  if (!fs.existsSync(realfilename)) {
    console.log({ [supplier_id]: filename });

    await writeFile(realfilename, page, endpoint)
      .then(res => {
        let { page, hasNextPage } = res;
        //console.log(JSON.stringify({ supplier_id, pages, page, hasNextPage }));
      })
      .catch(err => {
        console.error(JSON.stringify({ supplier_id, page, err }));
      });
  }
};

const getInfo = async endpoint => {
  const { supplier_id, url } = endpoint;
  const token = await getToken(endpoint);
  const query = { page: 1, pageSize: 1 };

  /* if (token.status !== 200) {
    console.log(supplier_id, token);
    return;
  } */

  const { token_type, access_token } = token.data;
  const info = await getData(url, query, token_type, access_token);

  if (info.status !== 200 || info.data.code || typeof info.data === 'undefined') {
    console.error(`Error en ${supplier_id}`, info);
    return;
  } else {
    const { totalRows } = info.data.pagination;

    let num = Math.floor(totalRows / pageSizeDefault);
    let pages = totalRows % pageSizeDefault ? num + 1 : num;
    let linfo = { supplier_id, totalRows, pages };
    console.log(linfo);
  
    let dir = `${__dirname}/data/${supplier_id}`;
    let step = 1;
    const maxPage = pages + 1;
  
    for (let page = 1; page < maxPage; page += step) {
      let prom = [];
      for (let index = 0; index < 5 && index + page < maxPage; index++) {
        let filename = `data-${String(page).padStart(10, '0')}.json`;
        let realfilename = `${dir}/${filename}`;
  
        if (!fs.existsSync(realfilename)) {
          prom.push(download(page + index, dir, supplier_id, endpoint, pages));
          //console.log(prom)
        }
      }
      await Promise.allSettled(prom);
    }
    console.log({ Finaliza: supplier_id });
  }


};

const init = () => {
  endpoints.forEach(async e => {
    /* if (e.download) {
      const sup_dir = `${__dirname}/data/${e.supplier_id}`;
      if (!fs.existsSync(sup_dir)) fs.mkdirSync(sup_dir, { recursive: true });
      await getInfo(e);
    } else {
      console.error(`${e.supplier_id} NO tiene habilitida la descarga`)
    } */
    const sup_dir = `${__dirname}/data/${e.supplier_id}`;
    if (!fs.existsSync(sup_dir)) fs.mkdirSync(sup_dir, { recursive: true });
    await getInfo(e);
  });
};

init();
