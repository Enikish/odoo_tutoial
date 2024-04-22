/** @odoo-module **/
import { Component, useState, xml, markup } from "@odoo/owl"


export class Card extends Component{
    static template = 'awesome_owl.card';
    static props = {
        title: String,
        content: String,
    };
    value1 = "<div>some text 1</div>";
    value2 = markup("<div><a href='https://www.baidu.com'>some text 2</a></div>");
}