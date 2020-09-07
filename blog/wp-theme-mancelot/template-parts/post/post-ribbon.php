<?php
/**
 * Display post ribbon in single page only.
 *
 * @package cenote.
 */

$type            = get_theme_mod( 'cenote_post_ribbon_category_select', 'tg-post-latest' );
$category_select = get_theme_mod( 'cenote_post_ribbon_categories', 'cenote_all_category' );
if ( 'cenote_all_category' === $category_select ) {
	$category_select = false;
}

?>
<div class="tg-post-ribbon">
	<div class="tg-container">
		<?php
		// Options.
		$args = array(
			'posts_per_page'      => 4,
			'post_type'           => 'post',
			'ignore_sticky_posts' => true,
			'no_found_rows'       => true,
		);

		// If category is selected, make post load from category.
		if ( 'tg-post-category' === $type ) :
			$args['category__in'] = $category_select;
		endif;

		$query_ribbon_posts = new WP_Query( $args );
		?>

		<ul id="tg-post-ribbon-container" class="tg-flex-container tg-post-ribbon-wrapper">

			<?php
			while ( $query_ribbon_posts->have_posts() ) :
				$query_ribbon_posts->the_post();
				?>

				<li>
					<?php if ( has_post_thumbnail() ) : ?>
						<a class="tg-post-thumbnail tg-post-ribbon-thumbnail" href="<?php the_permalink( $post->ID ); ?>"><?php the_post_thumbnail( 'thumbnail' ); ?></a>
					<?php endif; ?>
					<div class="tg-post-info tg-posts-ribbon-info">
						<a href="<?php the_permalink( $post->ID ); ?>" class="tg-post-title"><?php the_title(); ?></a>
						<span class="post-date"><?php echo get_the_date(); ?></span>
					</div>
				</li>
			<?php
			endwhile;
			?>

		</ul>
		<?php
		wp_reset_postdata();
		?>
	</div>
	<!-- /.post-ribbon-wrapper -->
</div>
<!-- /.tg-ribbon -->
