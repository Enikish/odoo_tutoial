/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./Todo/TodoList";
import { TodoItem } from "./Todo/TodoItem";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList, TodoItem };
    setup(){    
        this.state = useState({ sum: 2});
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum(){
        this.state.sum++;
    }
}
