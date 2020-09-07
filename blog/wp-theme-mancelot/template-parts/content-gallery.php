<?php
/**
 * Template part for displayinng gallery post format.
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$gallery                = get_post_gallery( get_the_ID(), false );
$gallery_attachment_ids = explode( ',', $gallery['ids'] );
$layout_style           = cenote_is_layout();
$thumbnail_size         = 'post-thumbnail';
$archive_style          = get_theme_mod( 'cenote_archive_style', 'tg-archive-style--masonry' );

if ( 'tg-archive-style--classic' === $archive_style && 'layout--no-sidebar' === $layout_style ) {
	$thumbnail_size = 'cenote-full-width';
}
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<?php if ( ! empty( $gallery_attachment_ids ) ) : ?>
		<div class="post-format-media post-format-media--gallery">
			<div class="post-format-gallery swiper-container">
				<div class="swiper-wrapper">
					<?php foreach ( $gallery_attachment_ids as $gallery_attachment_id ) : ?>
						<div class="post-format-gallery-item swiper-slide">
							<?php echo wp_get_attachment_image( $gallery_attachment_id, $thumbnail_size ); // WPCS xss ok. ?>
						</div>
					<?php endforeach; ?>
				</div>
				<!-- /.post-format-gallery -->
				<div class="swiper-button-next"></div>
				<div class="swiper-button-prev"></div>
			</div>
			<!-- /.post-format-media -->
		</div>
	<?php endif; ?>
	<!-- /.post-format-media post-format-media--gallery -->
	<!-- /.post-format-media post-format-media--galery -->
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
