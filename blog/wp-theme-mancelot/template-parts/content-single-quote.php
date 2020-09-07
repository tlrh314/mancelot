<?php
/**
 * Template part for displaying single quote post format
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$content_orders = get_theme_mod( 'cenote_single_order_layout', array( 'thumbnail', 'categories', 'title', 'meta', 'content', 'footer' ) );
$gallery_images = get_post_gallery_images();
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<div class="entry-content">
		<?php
		the_content();

		wp_link_pages(
			array(
				'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'cenote' ),
				'after'  => '</div>',
			)
		);
		?>
	</div>
	<!-- /.entry-content -->

	<?php cenote_post_thumbnail(); ?>

	<div class="tg-top-cat">
		<?php cenote_post_categories(); ?>
	</div>

	<header class="entry-header">
		<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
	</header><!-- .entry-header -->

	<div class="entry-meta">
		<?php
			cenote_posted_by();
			cenote_posted_on();
		?>
	</div><!-- .entry-meta -->

	<footer class="entry-footer">
		<?php cenote_entry_footer(); ?>
	</footer><!-- .entry-footer -->

	<?php
	// Show author box if enabled.
	if ( true === get_theme_mod( 'cenote_single_enable_author_box', true ) ) {
		get_template_part( 'template-parts/author/author', 'box' );
	}
	?>
</article><!-- #post-<?php the_ID(); ?> -->
