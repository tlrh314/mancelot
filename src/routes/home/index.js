import { h } from 'preact';
import style from './style';

const Home = () => (
	<div class={style.home}>
		<div class="header_home"></div>
		<h1>Waar ben je naar op zoek?</h1>
		<div class="category_man"></div>
		<div class="footer">
			<div class="btn_settings"></div>
			<div class="btn_info"></div>
			<div class="poweredby">Powered by Project Cece</div>
		</div>
	</div>
);

export default Home;
