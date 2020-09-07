<?php
/**
 * Template part for displaying page content in page.php
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$content_orders = get_theme_mod( 'cenote_page_order_layout', array( 'title', 'thumbnail', 'content', 'footer' ) );
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
<?php foreach ( $content_orders as $key => $content_order ) : ?>
	<?php if ( 'title' === $content_order ) : ?>
		<header class="entry-header">
			<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
		</header><!-- .entry-header -->
	<?php endif; ?>

	<?php if ( 'thumbnail' === $content_order ) : ?>
		<?php cenote_post_thumbnail(); ?>
	<?php endif; ?>

	<?php if ( 'content' === $content_order ) : ?>
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
	<?php endif; ?>

	<?php if ( 'footer' === $content_order && get_edit_post_link() ) : ?>
		<footer class="entry-footer">
			<?php
				edit_post_link(
					sprintf(
						wp_kses(
							/* translators: %s: Name of current post. Only visible to screen readers */
							__( 'Edit <span class="screen-reader-text">%s</span>', 'cenote' ),
							array(
								'span' => array(
									'class' => array(),
								),
							)
						),
						get_the_title()
					),
					'<span class="edit-link">',
					'</span>'
				);
			?>
		</footer><!-- .entry-footer -->
	<?php endif; ?>
<?php endforeach; ?>
</article><!-- #post-<?php the_ID(); ?> -->
