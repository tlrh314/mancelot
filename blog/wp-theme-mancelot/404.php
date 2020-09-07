<?php
/**
 * The template for displaying 404 pages (not found)
 *
 * @link https://codex.wordpress.org/Creating_an_Error_404_Page
 *
 * @package cenote
 */

get_header(); ?>

	<div id="primary" class="content-area">
		<main id="main" class="site-main">

			<section class="error-404 not-found">
				<img  class="error-img" src="<?php echo esc_url( get_template_directory_uri() ); ?>/assets/img/404.svg" alt="">
				<header class="page-header">
					<h1 class="page-title"><?php esc_html_e( 'Sorry, but nothing exists here.', 'cenote' ); ?></h1>
				</header><!-- .page-header -->

				<div class="page-content">
					<p><?php esc_html_e( 'Try searching or ', 'cenote' ); ?><a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home"><?php esc_html_e( 'Go back to Home', 'cenote' ); ?></a></p>

					<div class="error-404__search">
					<?php
						get_search_form();
					?>
					</div>
				</div><!-- .page-content -->
			</section><!-- .error-404 -->

		</main><!-- #main -->
	</div><!-- #primary -->

<?php
get_footer();
