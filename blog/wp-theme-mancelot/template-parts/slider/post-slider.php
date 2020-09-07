<?php
/**
 * Template for displaying post slider
 *
 * Shows slider on top part
 *
 * @package cenote
 */

$type              = get_theme_mod( 'cenote_post_slide_category', 'latest-post' );
$selected_category = get_theme_mod( 'cenote_post_slide_category_select', 'uncategorized' );
?>

<div class="tg-slider tg-post-slider <?php echo esc_attr( 'tg-post-slider--carousel' ); ?>">
	<div class="tg-container">
		<div class="swiper-container">
			<div class="swiper-wrapper">
				<?php
				// Options.
				$args = array(
					'posts_per_page'      => 6,
					'post_type'           => 'post',
					'ignore_sticky_posts' => true,
					'no_found_rows'       => true,
				);

				// If category is selected, make post load from category.
				if ( 'category' === $type ) :
					$args['category__in'] = $selected_category;
				endif;

				$query_slider_posts = new WP_Query( $args );

				while ( $query_slider_posts->have_posts() ) :
					$query_slider_posts->the_post();
					$thumbnail = '';
					if ( has_post_thumbnail() ) {
						$thumbnail = 'style="background-image: url(' . get_the_post_thumbnail_url( get_the_ID(), 'cenote_slider' ) . ')"';
					}
					?>
					<div class="swiper-slide" <?php echo $thumbnail; // WPCS: XSS OK. ?>>
						<?php if ( has_post_thumbnail() ) : ?>
							<figure>
							<?php the_post_thumbnail( 'cenote-slider' ); ?>
							</figure>
						<?php endif; ?>
						<div class="tg-slider-container tg-flex-container tg-flex-item-centered">
						<?php the_title( '<h2 class="entry-title"><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">', '</a></h2>' ); ?>
							<div class="entry-meta">
								<?php
								cenote_post_categories();
								cenote_posted_on();
								?>
							</div>
						</div>
					</div>
					<?php
				endwhile;
				wp_reset_postdata();
				?>
			</div>
			<!-- /.swiper-wrapper -->
				<!-- If we need navigation buttons -->
				<div class="swiper-button-prev"></div>
				<div class="swiper-button-next"></div>
			<!-- /.tg-container -->
		</div>
		<!-- /.swiper-container -->
	</div>
</div>
<!-- /.tg-slider -->
