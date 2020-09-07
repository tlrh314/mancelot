<?php
/**
 * Template part for displayinng video post format.
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$content = apply_filters( 'the_content', get_the_content() );
$video   = get_media_embedded_in_content( $content, array( 'video', 'object', 'embed', 'iframe' ) );
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<div class="post-format-media post-format-media--video">
		<?php if ( ! empty( $video ) ) : ?>
			<div class="post-format-video">
				<?php echo $video[0]; // WPCS xss ok. ?>
			</div>
		<?php endif; ?>
	</div>
	<!-- /.post-format-media post-format-media--video -->
	<header class="entry-header">
		<?php the_title( '<h2 class="entry-title"><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">', '</a></h2>' ); ?>
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
