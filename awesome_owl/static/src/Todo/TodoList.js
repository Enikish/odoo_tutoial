/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./TodoItem";

export class TodoList extends Component{
    static template = "awesome_owl.todolist";
    static components = { TodoItem };
    
    setup() {
        this.todos = useState([
            {id: 0, description: "Check list", isCompleted: true},
            {id: 1, description: "Write tutorial", isCompleted: false},
            {id: 2, description: "Buy milk", isCompleted: true},
        ])
    }

}