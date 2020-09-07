<?php
/**
 * Template part for displayinng link post format.
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<header class="entry-header">
		<div class="post-format-media post-format-media--link">
			<?php the_title( '<a href="' . esc_url( cenote_get_link_url() ) . '" class="post-format-link" rel="bookmark"><h2 class="post-format-title">', '</h2></a>' ); ?>
		</div>
		<!-- /.post-format-media post-format-media--link -->
	</header><!-- .entry-header -->

	<div class="entry-meta">
		<?php
			cenote_post_categories();
			cenote_posted_on();
		?>
	</div><!-- .entry-meta -->

	<footer class="entry-footer">
		<a href="<?php the_permalink(); ?>" class="tg-readmore-link"><?php esc_html_e( 'Read More', 'cenote' ); ?></a>
	</footer><!-- .entry-footer -->
</article><!-- #post-<?php the_ID(); ?> -->
