import { h } from 'preact';
import { Link } from 'preact-router';
import style from './style';

const Firstuse = () => (
	<div class="firstuse">
		<div class="header_home"></div>
		<div class="content">
			<div class="slider-container">
			<slider>

				<card>
				<div class="firstuse_text">Mancelot maakt het mannen zoals jij<br /> <span>supermakkelijk</span> <br />om je kleding verantwoord te maken, want...</div>
				</card>

				<card>
				<div class="firstuse_text">...we bieden in deze simpele app een<br /> <span>grote collectie</span> <br />van verantwoorde merken!<br /><br />Hmm.. is dat niet ook heel duur?</div>
				</card>

				<card>
				<div class="firstuse_text"><span>Niet bij ons!</span> <br />Je 'doneert' slechts een paar euro per maand om structureel vele levens in de kledingindustrie te verbeteren en...</div>
				</card>

				<card>
				<div class="firstuse_text">...daarmee bouw je tegelijk een tegoed op, waarmee je verantwoorde kleding kunt uitkiezen!<br /><span>Beter voor jou en voor de wereld!</span></div>
				</card>
			</slider>
			</div>

		</div>
	</div>

);

export default Firstuse;
