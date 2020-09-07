<?php
/**
 * Template part for displaying single link post format
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$gallery                = get_post_gallery( get_the_ID(), false );
$gallery_attachment_ids = explode( ',', $gallery['ids'] );
$layout_style           = cenote_is_layout();
$thumbnail_size         = 'post-thumbnail';

if ( 'layout--no-sidebar' === $layout_style ) {
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
				<!-- /.post-format-media -->
				<div class="swiper-button-next"></div>
				<div class="swiper-button-prev"></div>
			</div>
			<!-- /.post-format-gallery -->
		</div>
	<?php endif; ?>
	<!-- /.post-format-media post-format-media--gallery -->

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
