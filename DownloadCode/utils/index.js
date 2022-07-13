'use strict';
const axiosp = require('axios');
const https = require('https');
const qs = require('qs');
require('dotenv').config();

const axios = axiosp.create({
  httpsAgent: new https.Agent({
    rejectUnauthorized: false
  })
});

const peticion = async opts => {
  return await axios(opts)
    .then(res => {
      let { status, data } = res;
      return { status, data };
    })
    .catch(err => {
      if (err.status) {
        return { status: err.status, data: err.response.data };
      } else {
        return { status: 500, data: `${err.syscall} ${err.code} ${err.hostname}` };
      }
    });
};

const getToken = async ({ username, password, scope, token_url, client_id, client_secret }) => {
  let data = { grant_type: 'password', username, password, client_id, client_secret };

  if (scope !== '') data.scope = scope;

  const opts = {
    url: token_url,
    method: 'post',
    auth: {
      username: client_id,
      password: client_secret
    },
    responseType: 'json',
    data: decodeURI(qs.stringify(data)),
    json: true
  };

  return await peticion(opts);
};

const getData = async (url, data, token_type, access_token) => {
  const opts = {
    url: url,
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `${token_type} ${access_token}`
    },
    data: data,
    json: true
  };

  return await peticion(opts);
};

module.exports = {
  getToken,
  getData
};
