import {h, Component} from 'preact';
import {route} from "preact-router";

export default class Overview extends Component {

    render({ colour }) {
        return (
            <div id="app">
                <div class="btn_back_container">
                    <button class="btn_back" onClick={e => route('/colourselection')}></button>
                </div>
                <h1>Overview voor de gekozen kleur {colour}</h1>
            </div>

        );
    }
}
