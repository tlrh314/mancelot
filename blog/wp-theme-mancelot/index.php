<?php
/**
 * The main template file
 *
 * This is the most generic template file in a WordPress theme
 * and one of the two required files for a theme (the other being style.css).
 * It is used to display a page when nothing more specific matches a query.
 * E.g., it puts together the home page when no home.php file exists.
 *
 * @link    https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package cenote
 */

$archive_layout = get_theme_mod( 'cenote_archive_style', 'tg-archive-style--masonry' );
get_header();
?>

	<div id="primary" class="content-area">
		<main id="main" class="site-main">

			<?php
			if ( have_posts() ) :
				if ( 'tg-archive-style--masonry' === $archive_layout ) :
					?>
					<div class="cenote-content-masonry cenote-content-masonry--animated">
					<div id="cenote-content-masonry">
				<?php
				endif;
				/* Start the Loop */
				while ( have_posts() ) :
					the_post();

					/*
					 * Include the Post-Format-specific template for the content.
					 * If you want to override this in a child theme, then include a file
					 * called content-___.php (where ___ is the Post Format name) and that will be used instead.
					 */
					get_template_part( 'template-parts/content', get_post_format() );

				endwhile;

				if ( 'tg-archive-style--masonry' === $archive_layout ) :
					?>
					</div>
					</div>
					<!-- /.cenote-content-masonry -->
				<?php
				endif;

				// show pagination.
				get_template_part( 'template-parts/pagination/pagination' );

			else :

				get_template_part( 'template-parts/content', 'none' );

			endif;
			?>

		</main><!-- #main -->
	</div><!-- #primary -->

<?php
get_sidebar();
get_footer();
