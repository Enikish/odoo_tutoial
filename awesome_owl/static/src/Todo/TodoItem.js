/** @odoo-module **/ 
import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component{
    static template = "awesome_owl.todoitem";

    static props = {
        id:{type: Number, optional: false},
        description:{type: String, optional: true},
        isCompleted:{type: Boolean, optional: false},
    }
}