<?php
/**
 * Template part for displaying posts
 *
 * @link    https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$content_orders = get_theme_mod( 'cenote_archive_order_layout', array(
	'thumbnail',
	'meta',
	'title',
	'content',
	'footer',
) );
$post_content   = get_theme_mod( 'cenote_archive_post_content', 'excerpt' );
$excerpt_count  = get_theme_mod( 'cenote_archive_excerpt_count', '40' );
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<?php
	foreach ( $content_orders as $key => $content_order ) :
		if ( 'thumbnail' === $content_order ) :
			cenote_post_thumbnail();
		elseif ( 'meta' === $content_order ) :
			?>
			<div class="entry-meta">
				<?php
				cenote_post_categories();
				cenote_posted_on();
				?>
			</div><!-- .entry-meta -->
		<?php
		elseif ( 'title' === $content_order ) :
			?>
			<header class="entry-header">
				<?php the_title( '<h2 class="entry-title"><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">', '</a></h2>' ); ?>
			</header><!-- .entry-header -->
		<?php

		elseif ( 'content' === $content_order ) :
			?>
			<div class="entry-content">
				<?php
				if ( 'excerpt' === $post_content ) {
					the_excerpt();
				} elseif ( 'content' === $post_content ) {
					the_content( sprintf(
						wp_kses(
							/* translators: %s: Name of current post. Only visible to screen readers */
							__( 'Continue reading<span class="screen-reader-text"> "%s"</span>', 'cenote' ),
							array(
								'span' => array(
									'class' => array(),
								),
							)
						),
						get_the_title()
					) );
				}
				?>
			</div><!-- .entry-content -->
		<?php
		elseif ( 'footer' === $content_order ) :
			?>
			<footer class="entry-footer">
				<a href="<?php the_permalink(); ?>" class="tg-readmore-link"><?php esc_html_e( 'Read More', 'cenote' ); ?></a>
			</footer><!-- .entry-footer -->
		<?php
		endif;
	endforeach;
	?>
</article><!-- #post-<?php the_ID(); ?> -->
