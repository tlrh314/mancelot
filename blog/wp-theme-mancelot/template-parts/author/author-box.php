<?php
/**
 * Displays Author bio on single post
 *
 * @package Cenote
 */

$author_id         = get_the_author_meta( 'ID' );
$author_avatar     = get_avatar( $author_id, 'thumbnail' );
$author_post_link  = get_the_author_posts_link();
$author_bio        = get_the_author_meta( 'description' );
$author_url        = get_the_author_meta( 'user_url' );
$author_post_count = count_user_posts( $author_id );

?>

<div class="tg-author-box">

	<?php if ( $author_avatar ) : ?>
		<div class="tg-author__avatar">
			<?php echo $author_avatar; // WPCS: XSS ok. ?>
		</div><!-- .tg-author-avatar -->
	<?php endif; ?>

	<div class="tg-author-info">
		<?php if ( $author_post_link ) : ?>
				<h5 class="tg-author__name"><?php echo $author_post_link; // WPCS: XSS ok. ?></h5>
			<?php endif; ?>

			<?php if ( $author_bio ) : ?>
			<div class="tg-author__bio">
				<?php echo wp_kses_post( $author_bio ); ?>
			</div><!-- .tg-author-bio -->
		<?php endif; ?>


		<div class="tg-author-meta">
			<?php if ( $author_url ) : ?>
				<div class="tg-author__website">
					<span><?php esc_html_e( 'Website', 'cenote' ); ?></span>
					<a href="<?php echo esc_url( $author_url ); ?>" target="_blank"><?php echo esc_url( $author_url ); ?></a>
				</div><!-- .tg-author-website -->
			<?php endif; ?>

			<?php if ( $author_post_count ) : ?>
				<div class="tg-author__post-count">
					<span><?php esc_html_e( 'Posts created', 'cenote' ); ?></span>
					<strong><?php echo intval( $author_post_count ); ?></strong>
				</div><!-- .tg-author-post-count -->
			<?php endif; ?>
		</div><!-- .tg-author-meta -->
	</div><!-- .tg-author-info -->
</div><!-- .tg-author-bio -->
