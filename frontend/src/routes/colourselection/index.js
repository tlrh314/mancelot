import {h, Component} from 'preact';
import {route} from 'preact-router';
import Grid from '../../components/grid';
import Productinfo from '../../components/productinfo';
import {addOrRemove} from "../../utils/collection/collection";

//TODO: verplaatsen van selectedColours naar store
export default class ColourSelection extends Component {

    state = {
        selectedColours: []
    };

    next = () => {
        const {selectedColours} = this.state;
        route(`/overview/${selectedColours.join('-')}`);
    };

    toggleColour = id => {
        const selectedColours = addOrRemove(this.state.selectedColours, id);
        this.setState({selectedColours});
    };

    render() {
        return (
            <div id="app">
                <div class="btn_back_container">
                    <button class="btn_back" onClick={() => route('/')}></button>
                </div>
                <h1>Wil je kleur bekennen?</h1>
                <h2>Je kunt meerdere kleuren kiezen</h2>
                <Grid
                    columnCount={3}
                    elementCount={12}
                    selectedElements={this.state.selectedColours}
                    onClick={this.toggleColour}
                />
                <div class="footer_bar">
                    <button class="btn_full" onClick={this.next}>Verder</button>
                </div>
            </div>

        );
    }
}
