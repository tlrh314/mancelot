<?php
/**
 * Template part for displaying single post
 *
 * @link    https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$content_orders = get_theme_mod( 'cenote_single_order_layout', array(
	'thumbnail',
	'categories',
	'title',
	'meta',
	'content',
	'footer',
) );
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<?php
	foreach ( $content_orders as $key => $content_order ) :
		if ( 'thumbnail' === $content_order ) :
			cenote_post_thumbnail();
		elseif ( 'categories' === $content_order ) :
			?>
			<div class="tg-top-cat">
				<?php cenote_post_categories(); ?>
			</div>
		<?php
		elseif ( 'title' === $content_order ) :
			?>
			<header class="entry-header">
				<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
			</header><!-- .entry-header -->
		<?php

		elseif ( 'meta' === $content_order && 'post' === get_post_type() ) :
			?>
			<div class="entry-meta">
				<?php
				cenote_posted_by();
				cenote_posted_on();
				?>
			</div><!-- .entry-meta -->
		<?php
		elseif ( 'content' === $content_order ) :
			?>
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
			</div><!-- .entry-content -->
		<?php
		elseif ( 'footer' === $content_order ) :
			?>
			<footer class="entry-footer">
				<?php cenote_entry_footer(); ?>
			</footer><!-- .entry-footer -->
		<?php
		endif;
	endforeach;

	// Show author box if enabled.
	if ( true === get_theme_mod( 'cenote_single_enable_author_box', true ) ) {
		get_template_part( 'template-parts/author/author', 'box' );
	}
	?>
</article><!-- #post-<?php the_ID(); ?> -->
