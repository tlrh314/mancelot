<?php
/**
 * The template for displaying all single posts
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/#single-post
 *
 * @package cenote
 */

 get_header(); ?>

	<div id="primary" class="content-area">
		<main id="main" class="site-main">

			<?php
			while ( have_posts() ) :
				the_post();

				get_template_part( 'template-parts/content-single', get_post_format() );

				$args = array(
					'prev_text' => '<span class="nav-links__label">' . esc_html__( 'Previous Article', 'cenote' ) . '</span> %title',
					'next_text' => '<span class="nav-links__label">' . esc_html__( 'Next Article', 'cenote' ) . '</span> %title',
				);

				the_post_navigation( $args );

				// If comments are open or we have at least one comment, load up the comment template.
				if ( comments_open() || get_comments_number() ) :
					comments_template();
				endif;

			endwhile; // End of the loop.
			?>

		</main><!-- #main -->
	</div><!-- #primary -->

<?php
get_sidebar();
get_footer();
