// ==UserScript==
// @name         华科HUST专选选课网页选课按钮强制显示
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  拦截 /zyxxk/Stuxk/getStuNowXkfs 的响应，并修改data内字段值为1
// @author       potatoshred
// @match        *://wsxk.hust.edu.cn/zyxxk/Stuxk/*
// @require      https://unpkg.com/ajax-hook@3.0.3/dist/ajaxhook.min.js
// @run-at       document-start
// @grant        none
// ==/UserScript==

(function () {
    'use strict';
    if (typeof ah === 'undefined') return;

    ah.proxy({
        onResponse: (response, handler) => {
            try {
                // 判断是否为需要拦截的请求
                if (response.config.url.includes('getStuNowXkfs')) {
                    let respData = JSON.parse(response.response);
                    // 修改响应数据
                    if (respData.data) {
                        // respData.data.akcxType = 1;
                        // respData.data.azxType = 1;
                        respData.data.aktxType = 1;
                    }
                    // 将修改后的数据写回response
                    response.response = JSON.stringify(respData);
                    console.log('已成功修改接口响应:', respData);
                }
            } catch (e) {
                console.error('处理响应时出错:', e);
            }
            handler.next(response);
        }
    });
})();