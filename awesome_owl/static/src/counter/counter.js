/** @odoo-module **/
import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = 'awesome_owl.Counter';
    static props = {
        value: Number,
        onChange: { type: Function, optional: true},
    }

    setup(){
        this.state = useState({ value : 0, flag : true});
    }

    increment(){
        this.state.value++;
        this.state.flag = !this.state.flag;
        this.props.onChange();
    }

    clear(){
        this.state.value = 0;
    }

}