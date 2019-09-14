import { h } from 'preact';
import { Link } from 'preact-router';
import style from './style';

const About = () => (
	<div class="about">
	<div class="btn_back_container">
			<Link href="/home"><button class="btn_back" onClick={e => route('/home')}></button> </Link>
	</div>
	<div class="header_home"></div>
		<div class="content">
			<p>Mancelot is een stichting, wij hebben geen winstoogmerk, wij proberen de prijzen zo laag mogelijk te houden door in bulk in te kopen. Uiteraard niet ten koste van de arbeiders of milieu!</p>
			<p>De kleding die je ziet in Mancelot is afkomstig van Project Cece. Dat is de grootste verzamelwebsite voor verantwoorde kleding van Europa. Ook de labels, prijzen en de teksten over de merken zijn van hen overgenomen.<br />Uiteraard geven we daarom een klein deel van onze inkomsten door aan Project Cece.</p>
			<p>Mancelot is opgericht door 2 vrienden: Lorentz Stout en Roman Markovski. Beiden dertigers hebben een eigen bedrijf en jonge kinderen en wilden iets doen om de wereld van morgen te verbeteren en (kinderen van) kledingarbeiders ook een kans op een mooie toekomst te geven.</p>
			<p>Mancelot heeft geen commerciële banden met andere partijen en ook Project CeCe heeft geen aandelen of andere vormen van invloed op onze stichting.</p>
			<p>Meer weten? Bekijk onze FAQ op <a href="https://www.mancelot.nl">mancelot.nl</a> of neem via de website contact op.</p>
			<div class="button">
			ALLEEN INDIEN NOG NIET AANGEMELD KNOP: Nu aanmelden
			</div>
		</div>

	</div>
);

export default About;
