import { h } from 'preact';
import { Link } from 'preact-router';
import style from './style';

//TODO: later mannetje in delen opsplitsen zodat shirt los kan animeren, lange broek en jas vouwen uit.
//TODO: er zit wel veel herhaling in onderstaande html. Oplossen d.m.v. simpel compoment
const Home = () => (
	<div class={style.home}>
		<div class="header_home"></div>
		<h1>Waar ben je naar op zoek?</h1>
		<div class="home_category_container">

			<div class="category_label shirt">
				<Link href="/colourselection"><span>Shirt</span><span class="small">en overhemd</span></Link>
				<div class="line"></div>
			</div>
			<div class="category_label jack"><span>Jas, trui</span><span class="small">en colbert</span><div class="line"></div></div>
			<div class="category_label short"><span>Korte broek</span><span class="small">en onderbroek</span><div class="line"></div></div>
			<div class="category_label long"><span>Lange broek</span><div class="line"></div></div>
			<div class="category_label sock"><span>Sokken</span><div class="line"></div></div>
			<div class="category_label shoe"><span>Schoenen</span><div class="line"></div></div>
		</div>

		<div class="footer">
			<div class="btn_settings"></div>
			<div class="btn_info"></div>
			<div class="poweredby">Powered by Project Cece</div>
		</div>
	</div>
);

export default Home;
