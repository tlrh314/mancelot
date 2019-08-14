import { h, Component } from 'preact';
import { route } from 'preact-router';
import Grid from '../../components/grid';
import Productinfo from '../../components/productinfo';

export default class ColourSelection extends Component {

	colourSelected = id => {
		route(`/overview/${id}`);
	};

	render() {
		return (
			<div id="app">
				<div class="btn_back_container">
					<button class="btn_back" onClick={ () => route('/') }></button>
				</div>
				<h1>Wil je kleur bekennen?</h1>
				<h2>Je kunt meerdere kleuren kiezen</h2>
				<Grid
					columnCount={3}
					elementCount={12}
					onClick={this.colourSelected}
				/>
				<Productinfo />

				<div class="footer_bar"><button class="btn_full" onClick={ e => alert("nice animation starts here!") }>Verder</button></div>
			</div>

		);
	}
}
