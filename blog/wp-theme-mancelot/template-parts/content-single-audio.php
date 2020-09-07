<?php
/**
 * Template part for displaying single video post format
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$content = apply_filters( 'the_content', get_the_content() );
$audio   = get_media_embedded_in_content( $content, array( 'audio', 'iframe' ) );
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>

	<div class="post-format-media post-format-media--audio">
		<?php if ( ! empty( $audio ) ) : ?>
			<div class="post-format-audio">
				<?php echo $audio[0]; // WPCS xss ok. ?>
			</div>
		<?php endif; ?>
	</div>
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
