<?php
/**
 * Template for displaying content of related post.
 *
 * @package cenote
 */

$related_post_class = '';
if ( has_post_thumbnail() ) {
	$related_post_class = 'has-post-thumbnail';
}
?>
<article id="post-<?php the_ID(); ?>" class="related-post-item <?php echo esc_attr( $related_post_class ); ?>">
	<?php cenote_related_post_thumbnail(); ?>
	<div class="entry-meta">
		<?php
			cenote_post_categories();
			cenote_posted_on();
		?>
	</div><!-- .entry-meta -->

	<header class="entry-header">
		<?php the_title( '<h2 class="entry-title"><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">', '</a></h2>' ); ?>
	</header><!-- .entry-header -->

</article><!-- #post-<?php the_ID(); ?> -->
