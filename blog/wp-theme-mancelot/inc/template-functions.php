<?php
/**
 * Functions which enhance the theme by hooking into WordPress
 *
 * @package cenote
 */

/**
 * Add a pingback url auto-discovery header for singularly identifiable articles.
 */
function cenote_pingback_header() {
	if ( is_singular() && pings_open() ) {
		echo '<link rel="pingback" href="', esc_url( get_bloginfo( 'pingback_url' ) ), '">';
	}
}

add_action( 'wp_head', 'cenote_pingback_header' );


/**
 * Checks if the current page matches the given layout
 *
 * @return string $layout layout of current page.
 */
function cenote_is_layout() {
	global $post;
	$layout = '';

	if ( is_archive() || is_home() ) {
		$layout = get_theme_mod( 'cenote_layout_archive', 'layout--no-sidebar' );
	} elseif ( is_single() ) {
		$individual_layout = get_post_meta( $post->ID, 'cenote_post_layout', true );

		// If individual layout is set.
		if ( ! empty( $individual_layout ) ) {
			$layout = $individual_layout;
		} else {
			// if individual layout is not set add global one.
			$layout = get_theme_mod( 'cenote_layout_single', 'layout--right-sidebar' );
		}
	} elseif ( is_page() ) {
		$individual_layout = get_post_meta( $post->ID, 'cenote_post_layout', true );

		// If individual layout is set.
		if ( ! empty( $individual_layout ) ) {
			$layout = $individual_layout;
		} else {
			// if individual layout is not set add global one.
			$layout = get_theme_mod( 'cenote_layout_page', 'layout--right-sidebar' );
		}
	}

	return $layout;
}

/**
 * Retuns the post url
 *
 * @return string the link format url.
 */
function cenote_get_link_url() {
	$content = get_the_content();
	$has_url = get_url_in_content( $content );
	return ( $has_url ) ? $has_url : apply_filters( 'the_permalink', get_permalink() );
}

/**
 * Adds the necessary template to load on footer.
 *
 * @return void
 */
function cenote_add_footer_extras() {
	$menu_style = get_theme_mod( 'cenote_menu_style', 'tg-site-menu--default' );

	// Load mobile navigaiton.
	get_template_part( 'template-parts/menu/menu', 'mobile' );

	// Load offcanvas or full screen menu.
	if ( 'tg-site-menu--offcanvas' === $menu_style || 'tg-site-menu--fullscreen' === $menu_style ) {
		get_template_part( 'template-parts/menu/menu', 'primary' );
	}

	// load search form.
	get_template_part( 'template-parts/footer/search', 'form' );

	// Show back to top if enabled.
	if ( true === get_theme_mod( 'cenote_footer_enable_back_to_top', true ) ) {
		?>
		<div id="cenote-back-to-top" class="cenote-back-to-top">
		<span>
			<?php esc_html_e( 'Back To Top', 'cenote' ); ?>
			<i class="tg-icon-arrow-right"></i>
		</span>
	</div>
	<?php
	}
}
add_action( 'cenote_after_footer', 'cenote_add_footer_extras' );

/**
 * Adds elements after header
 */
function cenote_add_after_header() {
	// Show sticky header if enabled.
	if ( true === get_theme_mod( 'cenote_header_sticky_option', true ) ) :
		get_template_part( 'template-parts/header/header', 'sticky' );
	endif;
}
add_action( 'cenote_after_header', 'cenote_add_after_header' );

/**
 * Adds post slider.
 *
 * @return void
 */
function cenote_add_post_slider() {
	// Show post slider if enabled.
	if ( ( is_home() || is_front_page() ) && true === get_theme_mod( 'cenote_post_slider_enabled', false ) ) :
		get_template_part( 'template-parts/slider/post', 'slider' );
	endif;
}

add_action( 'cenote_after_header', 'cenote_add_post_slider', 5 );

/**
 * Adds breadcrumb to site if enabled.
 *
 * @return void
 */
function cenote_add_breadcrumnb() {
	// Show Breadcrumb if enabled.
	if ( true === get_theme_mod( 'cenote_breadcrumb', true ) ) :
		get_template_part( 'template-parts/breadcrumb/breadcrumb', 'trail' );
	endif;
}
add_action( 'cenote_after_header', 'cenote_add_breadcrumnb', 10 );

/**
 * Adds page header
 *
 * @return void
 */
function cenote_add_page_header() {
	if ( is_home() && ! is_front_page() ) {
		?>
			<header>
				<div class="tg-container">
						<h1 class="page-title screen-reader-text"><?php single_post_title(); ?></h1>
				</div>
			</header>
			<!-- /.tg-container -->
		<?php
	} elseif ( is_archive() ) {
		?>
		<header class="page-header">
			<div class="tg-container">
				<?php
					the_archive_title( '<h1 class="page-title">', '</h1>' );
					the_archive_description( '<div class="archive-description">', '</div>' );
				?>
			</div>
			<!-- /.tg-container -->
		</header><!-- .page-header -->
		<?php
	}
}
add_action( 'cenote_after_header', 'cenote_add_page_header' );

/**
 * Adds dropcap markup on the content.
 *
 * @param string $content the_content.
 * @return string $content
 */
function cenote_add_drop_cap_on_content( $content ) {
	$archive_style    = get_theme_mod( 'cenote_archive_style', 'tg-archive-style--masonry' );
	$archive_drop_cap = get_theme_mod( 'cenote_archive_enable_drop_cap', false );
	$single_drop_cap  = get_theme_mod( 'cenote_single_enable_drop_cap', true );

	// Return if the post format is link or quote.
	if ( in_array( get_post_format(), array( 'link', 'quote' ), true ) ) {
		return $content;
	}

	$pattern          = '/<p( .*)?( class="(.*)")??( .*)?>((<[^>]*>|\s)*)((&quot;|&#8220;|&#8216;|&lsquo;|&ldquo;|\')?[A-Z])/U';
	$replacement      = '<p$1 class="first-child $3"$4>$5<span title="$7" class="cenote-drop-cap">$7</span>';
	$content_filtered = preg_replace( $pattern, $replacement, $content, 1 );

	if ( is_single() && true === $single_drop_cap ) {
		$content = $content_filtered;
	}

	// If drop cap is enabled on archive( big block and classic ).
	if ( ( is_archive() || is_home() ) && true === $archive_drop_cap ) {
		$content = $content_filtered;
	}
	return $content;
}
add_filter( 'the_content', 'cenote_add_drop_cap_on_content' );


/**
 * Adds dropcap markup on excerpt
 *
 * @param string $excerpt the_excerpt.
 * @return string $excerpt
 */
function cenote_add_drop_cap_on_excerpt( $excerpt ) {
	$archive_style    = get_theme_mod( 'cenote_archive_style', 'tg-archive-style--masonry' );
	$archive_drop_cap = get_theme_mod( 'cenote_archive_enable_drop_cap', false );

	$pattern          = '/<p>([A-Z])/';
	$replacement      = '<p class="first-child"><span title="$1" class="cenote-drop-cap">$1</span>';
	$excerpt_filtered = preg_replace( $pattern, $replacement, $excerpt, 1 );

	if ( ( is_archive() || is_home() ) && true === $archive_drop_cap ) {
		$excerpt = $excerpt_filtered;
	}
	return $excerpt;
}
add_filter( 'the_excerpt', 'cenote_add_drop_cap_on_excerpt' );


/**
 * Adds post ribbon.
 *
 * @return void
 */
function cenote_add_post_ribbon() {
	// Show post ribbon if enabled.
	if ( is_single() && true === get_theme_mod( 'cenote_single_post_ribbon_display', false ) ) :
		get_template_part( 'template-parts/post/post', 'ribbon' );
	endif;
}

add_action( 'cenote_after_header', 'cenote_add_post_ribbon', 5 );

/**
 * Compare user's current version of plugin.
 */
if ( ! function_exists( 'cenote_plugin_version_compare' ) ) {
	function cenote_plugin_version_compare( $plugin_slug, $version_to_compare ) {
		if ( ! function_exists( 'get_plugins' ) ) {
			require_once ABSPATH . 'wp-admin/includes/plugin.php';
		}

		$installed_plugins = get_plugins();

		// Plugin not installed.
		if ( ! isset( $installed_plugins[ $plugin_slug ] ) ) {
			return false;
		}

		$tdi_user_version = $installed_plugins[ $plugin_slug ]['Version'];

		return version_compare( $tdi_user_version, $version_to_compare, '<' );
	}
}