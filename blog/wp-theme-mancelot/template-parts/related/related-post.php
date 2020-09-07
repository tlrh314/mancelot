<?php
/**
 * Shows related post on single page
 *
 * @package cenote
 */

global $post;
$post_id     = get_the_id();
$categories  = get_the_terms( $post_id, 'category' );
$updated_cat = array();

// Get only category slug of current post.
if ( $categories && is_array( $categories ) ) {
	foreach ( $categories as $category ) {
		$updated_cat[] = $category->term_id;
	}
}

// Query the posts.
$related_post = new WP_Query(
	array(
		'post_type'      => 'post',
		'posts_per_page' => 4,
		'orderby'        => 'rand', // phpcs:ignore
		'post__not_in'   => array( $post_id ),
		'category__in'   => $updated_cat,
	)
);

if ( $related_post->have_posts() ) :
	?>
	<section class="cenote-related-post">
		<div class="tg-container">
			<h2 class="related-post-title"><?php esc_html_e( 'Related Posts', 'cenote' ); ?></h2>
		</div>
		<!-- /.tg-container -->
		<!-- /.related-post-title -->
		<div class="cenote-related-post-container">
			<div class="tg-container">
				<div class="tg-flex-row tg-flex-container">
					<?php
					while ( $related_post->have_posts() ) :
						$related_post->the_post();
						get_template_part( 'template-parts/related/content', 'related' );
					endwhile;
					?>
				</div>
				<!-- /.tg-flex-row -->
			</div>
			<!-- /.tg-container tg-container-flex -->
		</div>
		<!-- /.cenote-related-post-container -->
	</section>
	<!-- /.cenote-related-post -->
	<?php
endif;
