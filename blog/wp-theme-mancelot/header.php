<?php
/**
 * The header for our theme
 *
 * This is the template that displays all of the <head> section and everything up until <div id="content">
 *
 * @link    https://developer.wordpress.org/themes/basics/template-files/#template-partials
 *
 * @package cenote
 */

?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
	<link rel="profile" href="http://gmpg.org/xfn/11">

	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>

<?php
if ( function_exists( 'wp_body_open' ) ) {
	wp_body_open();
}
?>

<div id="page" class="site">
	<a class="skip-link screen-reader-text" href="#content"><?php esc_html_e( 'Skip to content', 'cenote' ); ?></a>

	<header id="masthead" class="site-header tg-site-header <?php cenote_header_class(); ?>">
		<?php if ( true === get_theme_mod( 'cenote_enable_header_top', true ) ) : ?>
			<div class="tg-header-top">
				<div class="tg-container tg-flex-container tg-flex-space-between tg-flex-item-centered">
					<?php get_template_part( 'template-parts/header/header', 'top' ); ?>
				</div>
			</div><!-- .tg-header-top -->
		<?php endif; ?>

		<div class="tg-header-bottom">
			<?php get_template_part( 'template-parts/header/header', 'bottom' ); ?>
		</div>

	</header><!-- #masthead -->

	<?php do_action( 'cenote_after_header' ); ?>

	<div id="content" class="site-content">

		<div class="tg-container tg-flex-container tg-flex-space-between">
