<?php
/**
 * Template part for displaying single video post format
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$background_image = '';
if ( has_post_thumbnail() ) {
	$image_url        = get_the_post_thumbnail_url( $post->ID, 'full' );
	$background_image = 'style="background-image: url(' . $image_url . ');"';
}
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>

	<header class="entry-header entry-header--cover">
		<?php if ( has_post_thumbnail() ) : ?>
		<figure class="entry-thumbnail entry-thumbnail--template" <?php echo $background_image; // WPCS:XSS ok. ?>>
			<div class="entry-info">
				<div class="tg-top-cat">
					<?php cenote_post_categories(); ?>
				</div>
				<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>

				<div class="entry-meta">
					<?php
						cenote_posted_by();
						cenote_posted_on();
					?>
				</div><!-- .entry-meta -->
			</div>
			<!-- /.entry-info -->
		</figure>
		<?php endif; ?>
	</header><!-- .entry-header -->


	<div class="entry-center-content">
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
		$args = array(
			'prev_text' => '<span class="nav-links__label">' . esc_html__( 'Previous Article', 'cenote' ) . '</span> %title',
			'next_text' => '<span class="nav-links__label">' . esc_html__( 'Next Article', 'cenote' ) . '</span> %title',
		);

		// Show author box if enabled.
		if ( true === get_theme_mod( 'cenote_single_enable_author_box', true ) ) {
			get_template_part( 'template-parts/author/author', 'box' );
		}

		the_post_navigation( $args );

		// If comments are open or we have at least one comment, load up the comment template.
		if ( comments_open() || get_comments_number() ) :
			comments_template();
		endif;
		?>
	</div>
	<!-- /.entry-center-content -->
</article><!-- #post-<?php the_ID(); ?> -->
