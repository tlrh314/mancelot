<?php
/**
 * Custom template tags for this theme
 *
 * Eventually, some of the functionality here could be replaced by core features.
 *
 * @package cenote
 */

if ( ! function_exists( 'cenote_posted_on' ) ) :
	/**
	 * Prints HTML with meta information for the current post-date/time.
	 */
	function cenote_posted_on() {
		$time_string = '<time class="entry-date published updated" datetime="%1$s">%2$s</time>';
		if ( get_the_time( 'U' ) !== get_the_modified_time( 'U' ) ) {
			$time_string = '<time class="entry-date published" datetime="%1$s">%2$s</time><time class="updated" datetime="%3$s">%4$s</time>';
		}

		$time_string = sprintf(
			$time_string,
			esc_attr( get_the_date( 'c' ) ),
			esc_html( get_the_date() ),
			esc_attr( get_the_modified_date( 'c' ) ),
			esc_html( get_the_modified_date() )
		);

		$posted_on = sprintf(
			'%s',
			'<a href="' . esc_url( get_permalink() ) . '" rel="bookmark">' . $time_string . '</a>'
		);

		echo '<span class="posted-on">' . $posted_on . '</span>'; // WPCS: XSS OK.

	}
endif;

if ( ! function_exists( 'cenote_posted_by' ) ) :
	/**
	 * Prints HTML with meta information for the current author.
	 */
	function cenote_posted_by() {
		$byline = sprintf(
			'%s',
			'<span class="author vcard"><a class="url fn n" href="' . esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ) . '">' . esc_html( get_the_author() ) . '</a></span>'
		);

		echo '<span class="byline"> ' . $byline . '</span>'; // WPCS: XSS OK.

	}
endif;

if ( ! function_exists( 'cenote_entry_footer' ) ) :
	/**
	 * Prints HTML with meta information for the categories, tags and comments.
	 */
	function cenote_entry_footer() {
		// Hide category and tag text for pages.
		if ( 'post' === get_post_type() ) {
			/* translators: used between list items, there is a space after the comma */
			$categories_list = get_the_category_list( ' ' );
			if ( $categories_list ) {
				/* translators: 1: list of categories. */
				printf( '<span class="cat-links">' . esc_html__( 'Category: %1$s', 'cenote' ) . '</span>', $categories_list ); // WPCS: XSS OK.
			}

			$tags_list = get_the_tag_list( '', '' );
			if ( $tags_list ) {
				/* translators: 1: list of tags. */
				printf( '<span class="tags-links">' . esc_html__( 'Tagged: %1$s', 'cenote' ) . '</span>', $tags_list ); // WPCS: XSS OK.
			}
		}

		if ( ! is_single() && ! post_password_required() && ( comments_open() || get_comments_number() ) ) {
			echo '<span class="comments-link">';
			comments_popup_link(
				sprintf(
					wp_kses(
						/* translators: %s: post title */
						__( 'Leave a Comment<span class="screen-reader-text"> on %s</span>', 'cenote' ),
						array(
							'span' => array(
								'class' => array(),
							),
						)
					),
					get_the_title()
				)
			);
			echo '</span>';
		}

		edit_post_link(
			sprintf(
				wp_kses(
					/* translators: %s: Name of current post. Only visible to screen readers */
					__( 'Edit <span class="screen-reader-text">%s</span>', 'cenote' ),
					array(
						'span' => array(
							'class' => array(),
						),
					)
				),
				get_the_title()
			),
			'<span class="edit-link">',
			'</span>'
		);
	}
endif;

if ( ! function_exists( 'cenote_post_thumbnail' ) ) :
	/**
	 * Displays an optional post thumbnail.
	 *
	 * Wraps the post thumbnail in an anchor element on index views, or a div
	 * element when on single views.
	 */
	function cenote_post_thumbnail() {
		global $wp_query;
		$current_post = $wp_query->current_post;

		$thumbnail_size     = 'post-thumbnail';
		$archive_style      = get_theme_mod( 'cenote_archive_style', 'tg-archive-style--masonry' );
		$title_first_letter = substr( get_the_title(), 0, 1 );
		$layout_style       = cenote_is_layout();

		if ( post_password_required() || is_attachment() || ! has_post_thumbnail() ) {
			return;
		}

		// Change image size in block and big .
		if ( 'tg-archive-style--block' === $archive_style ) {
			$thumbnail_size = 'cenote-post';
		} elseif ( 'tg-archive-style--masonry' === $archive_style ) {
			$thumbnail_size = 'cenote-post-auto';
		} elseif ( 'tg-archive-style--classic' === $archive_style && 'layout--no-sidebar' === $layout_style ) {
			$thumbnail_size = 'cenote-full-width';
		} elseif ( 'tg-archive-style--big-block' === $archive_style ) {
			if ( 0 === $current_post ) {
				$thumbnail_size = 'cenote-full-width';
			} else {
				$thumbnail_size = 'cenote-post';
			}
		}
		?>
		<?php if ( is_singular() ) : ?>
			<div class="entry-thumbnail">
				<?php
				if ( 'layout--no-sidebar' === $layout_style ) {
					the_post_thumbnail( 'cenote-full-width' );
				} else {
					the_post_thumbnail();
				}
				?>
			</div><!-- .post-thumbnail -->
		<?php else : ?>

		<a class="entry-thumbnail" href="<?php the_permalink(); ?>" aria-hidden="true">
			<?php if ( ! empty( $title_first_letter ) ) : ?>
				<span class="post-thumbnail__letter">
					<?php echo esc_html( $title_first_letter ); ?>
				</span>
			<?php endif; ?>
			<?php
				the_post_thumbnail(
					$thumbnail_size, array(
						'alt' => the_title_attribute(
							array(
								'echo' => false,
							)
						),
					)
				);
			?>
		</a>
	<?php
	endif; // End is_singular().
	}
endif;

/**
 * Displays post thumbnail for related post
 */
function cenote_related_post_thumbnail() {
	$title_first_letter = substr( get_the_title(), 0, 1 );
	if ( post_password_required() || is_attachment() || ! has_post_thumbnail() ) {
		return;
	}
	?>
	<a class="entry-thumbnail" href="<?php the_permalink(); ?>" aria-hidden="true">
		<?php if ( ! empty( $title_first_letter ) ) : ?>
			<span class="post-thumbnail__letter">
				<?php echo esc_html( $title_first_letter ); ?>
			</span>
		<?php endif; ?>
		<?php
		the_post_thumbnail(
			'cenote-post', array(
				'alt' => the_title_attribute(
					array(
						'echo' => false,
					)
				),
			)
		);
		?>
	</a>
	<?php
}

/**
 *  Displays list of categories
 */
function cenote_post_categories() {
	if ( 'post' === get_post_type() ) {
		/* translators: used between list items, there is a space after the comma */
		$categories_list = get_the_category_list( '<span class="cat-seperator">, </span>' );
		if ( $categories_list ) {
			/* translators: 1: list of categories. */
			printf( '<span class="cat-links">' . '%1$s' . '</span>', $categories_list ); // phpcs:ignore
		}
	}
}
