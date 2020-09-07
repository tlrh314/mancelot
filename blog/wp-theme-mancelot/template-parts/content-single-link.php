<?php
/**
 * Template part for displaying single link post format
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$content_orders = get_theme_mod( 'cenote_single_order_layout', array( 'thumbnail', 'categories', 'title', 'meta', 'content', 'footer' ) );
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>

	<div class="post-format-media post-format-media--link">
		<?php the_title( '<a href="' . esc_url( cenote_get_link_url() ) . '" class="post-format-link" rel="bookmark"><h2 class="post-format-title">', '</h2></a>' ); ?>
	</div>
	<!-- /.post-format-media post-format-media--link -->

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
