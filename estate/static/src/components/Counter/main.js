/** @odoo-modulel **/

import { browser } from "@web/core/browser/browser";
import { mount, whenReady } from "@odoo/owl";
import { Counter } from "./counter";
import { templates } from "@web/core/assets";


whenReady( () => {
    mount(Counter, document.body, {templates, dev: true, name: "Estate Counter"});
});


function logError(ev){
    ev.preventDefault();
    let error = ev ?.error || ev.reason;

    if(error.seen){
        return;
    }
    error.seen = true;

    let errorMessage = error.stack;
    while(error.cause){
        errorMessage += "\nCaused by: "
        errorMessage += error.cause.stack;
        error = error.cause;
    }
    console.error(errorMessage);
}

browser.addEventListener("error", (ev) => {logError(ev)});
browser.addEventListener("unhandledrejection", (ev) => {logError(ev)});
