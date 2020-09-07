<?php
/**
 * Cenote functions and definitions
 *
 * @link    https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package cenote
 */

if ( ! function_exists( 'cenote_setup' ) ) :
	/**
	 * Sets up theme defaults and registers support for various WordPress features.
	 *
	 * Note that this function is hooked into the after_setup_theme hook, which
	 * runs before the init hook. The init hook is too late for some features, such
	 * as indicating support for post thumbnails.
	 */
	function cenote_setup() {
		/*
		 * Make theme available for translation.
		 * Translations can be filed in the /languages/ directory.
		 * If you're building a theme based on cenote, use a find and replace
		 * to change 'cenote' to the name of your theme in all the template files.
		 */
		load_theme_textdomain( 'cenote', get_template_directory() . '/languages' );

		// Add default posts and comments RSS feed links to head.
		add_theme_support( 'automatic-feed-links' );

		/*
		 * Let WordPress manage the document title.
		 * By adding theme support, we declare that this theme does not use a
		 * hard-coded <title> tag in the document head, and expect WordPress to
		 * provide it for us.
		 */
		add_theme_support( 'title-tag' );

		/*
		 * Enable support for Post Thumbnails on posts and pages.
		 *
		 * @link https://developer.wordpress.org/themes/functionality/featured-images-post-thumbnails/
		 */
		add_theme_support( 'post-thumbnails' );

		/**
		 * Enable support for post formats
		 *
		 * @link https://developer.wordpress.org/themes/functionality/post-formats/
		 */
		add_theme_support( 'post-formats', array( 'gallery', 'link', 'image', 'quote', 'video', 'audio' ) );

		// This theme uses wp_nav_menu() in one location.
		register_nav_menus(
			array(
				'tg-menu-primary'    => esc_html__( 'Primary', 'cenote' ),
				'tg-menu-header-top' => esc_html__( 'Header Top', 'cenote' ),
			)
		);

		/*
		 * Switch default core markup for search form, comment form, and comments
		 * to output valid HTML5.
		 */
		add_theme_support(
			'html5',
			array(
				'search-form',
				'comment-form',
				'comment-list',
				'gallery',
				'caption',
			)
		);

		// Set up the WordPress core custom background feature.
		add_theme_support(
			'custom-background',
			apply_filters(
				'cenote_custom_background_args',
				array(
					'default-color' => 'ffffff',
					'default-image' => '',
				)
			)
		);

		// Add theme support for selective refresh for widgets.
		add_theme_support( 'customize-selective-refresh-widgets' );

		/**
		 * Add support for core custom logo.
		 *
		 * @link https://codex.wordpress.org/Theme_Logo
		 */
		add_theme_support(
			'custom-logo',
			array(
				'height'      => 250,
				'width'       => 250,
				'flex-width'  => true,
				'flex-height' => true,
			)
		);

		add_editor_style();

		// Gutenberg wide layout support.
		add_theme_support( 'align-wide' );

		// Gutenberg block layout support.
		add_theme_support( 'wp-block-styles' );

		// Gutenberg editor support.
		add_theme_support( 'responsive-embeds' );


	}
endif;
add_action( 'after_setup_theme', 'cenote_setup' );

/**
 * Custom image sizes for theme.
 */
function cenote_image_sizes() {

	// Set default post thumbnail. 16:9.
	set_post_thumbnail_size( 768, 432, true );
	// Large full width image.
	add_image_size( 'cenote-full-width', 1160, 653, true );
	// 3:4.
	add_image_size( 'cenote-post', 600, 400, true );
	// Auto size.
	add_image_size( 'cenote-post-auto', 600, 9999, false );

}

add_action( 'after_setup_theme', 'cenote_image_sizes' );

/**
 * Set the content width based on the theme's design and stylesheet.
 */
if ( ! isset( $content_width ) ) {
	$content_width = 770;
}

/**
 * Set the content width in pixels, based on the theme's design and stylesheet.
 *
 * Set the content width as selected on the theme options.
 *
 * @global int $content_width
 */
function cenote_content_width() {
	global $post, $content_width;

	if ( $post ) {
		$layout = get_post_meta( $post->ID, 'cenote_post_layout', true );
	}

	if ( empty( $layout ) ) {
		$layout = 'layout--default';
	}

	$single_post_page_layout = get_theme_mod( 'cenote_layout_single', 'layout--right-sidebar' );
	$single_page_layout      = get_theme_mod( 'cenote_layout_page', 'layout--right-sidebar' );

	if ( 'layout--default' === $layout ) {
		if ( ( ( 'layout--no-sidebar' === $single_post_page_layout ) && is_single() ) || ( ( 'layout--no-sidebar' === $single_page_layout ) && is_page() ) ) {
			$content_width = 1160;
		} else {
			$content_width = 770;
		}
	} elseif ( 'layout--no-sidebar' === $layout ) {
		$content_width = 1160;
	} else {
		$content_width = 770;
	}
}

add_action( 'template_redirect', 'cenote_content_width' );

/**
 * Register widget area.
 *
 * @link https://developer.wordpress.org/themes/functionality/sidebars/#registering-a-sidebar
 */
function cenote_widgets_init() {
	register_sidebar(
		array(
			'name'          => esc_html__( 'Sidebar', 'cenote' ),
			'id'            => 'sidebar-1',
			'description'   => esc_html__( 'Add widgets here.', 'cenote' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer 1', 'cenote' ),
			'id'            => 'footer-sidebar-1',
			'description'   => esc_html__( 'Add widgets here to show on footer 1.', 'cenote' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer 2', 'cenote' ),
			'id'            => 'footer-sidebar-2',
			'description'   => esc_html__( 'Add widgets here to show on footer 2.', 'cenote' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer 3', 'cenote' ),
			'id'            => 'footer-sidebar-3',
			'description'   => esc_html__( 'Add widgets here to show on footer 3.', 'cenote' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer 4', 'cenote' ),
			'id'            => 'footer-sidebar-4',
			'description'   => esc_html__( 'Add widgets here to show on footer 4.', 'cenote' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);
}

add_action( 'widgets_init', 'cenote_widgets_init' );

/**
 * Enqueue scripts and styles.
 */
function cenote_scripts() {
	$suffix = ( defined( 'SCRIPT_DEBUG' ) && SCRIPT_DEBUG ) ? '' : '.min';

	wp_enqueue_style( 'cenote-style', get_stylesheet_uri() );
	wp_style_add_data( 'cenote-style', 'rtl', 'replace' );

	wp_enqueue_style( 'themegrill-icons', get_template_directory_uri() . '/assets/css/themegrill-icons' . $suffix . '.css', array(), '1.0' );

	wp_enqueue_style( 'fontawesome', get_template_directory_uri() . '/assets/css/all' . $suffix . '.css' );

	wp_enqueue_script( 'cenote-skip-link-focus-fix', get_template_directory_uri() . '/assets/js/skip-link-focus-fix' . $suffix . '.js', array(), '20151215', true );
	wp_enqueue_script( 'hammer', get_template_directory_uri() . '/assets/js/hammer' . $suffix . '.js', array(), '2.0.8', true );

	// Load Swiper on Gallery post format.
	wp_enqueue_script( 'swiper', get_template_directory_uri() . '/assets/js/swiper' . $suffix . '.js', array(), '4.2.0', true );
	wp_enqueue_style( 'swiper', get_template_directory_uri() . '/assets/css/swiper' . $suffix . '.css', '4.2.0' );

	// Load headroom if sticky header is enabled.
	if ( true === get_theme_mod( 'cenote_header_sticky_option', true ) ) {
		wp_enqueue_script( 'headroom', get_template_directory_uri() . '/assets/js/Headroom' . $suffix . '.js', array(), '0.9.4', true );
	}

	// Only load masonry script if enabled.
	if ( ( is_archive() || is_home() ) && 'tg-archive-style--masonry' === get_theme_mod( 'cenote_archive_style', 'tg-archive-style--masonry' ) ) {
		wp_enqueue_script( 'masonry', get_template_directory_uri() . '/assets/js/masonry.pkgd' . $suffix . '.js', array(), '4.2.0', true );
		wp_enqueue_script( 'imagesloaded', get_template_directory_uri() . '/assets/js/imagesloaded.pkgd' . $suffix . '.js', array(), '4.1.4', true );
	}

	wp_enqueue_script( 'cenote-custom', get_template_directory_uri() . '/assets/js/cenote-custom' . $suffix . '.js', array(), '1.0.0', true );

	if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
		wp_enqueue_script( 'comment-reply' );
	}
}

add_action( 'wp_enqueue_scripts', 'cenote_scripts' );

/**
 * Enqueue Google fonts and editor styles.
 */
function cenote_block_editor_styles() {
	wp_enqueue_style( 'cenote-editor-googlefonts', '//fonts.googleapis.com/css2?family=Roboto' );
	wp_enqueue_style( 'cenote-block-editor-styles', get_template_directory_uri() . '/style-editor-block.css' );
}

add_action( 'enqueue_block_editor_assets', 'cenote_block_editor_styles', 1, 1 );


/**
 * Implement the Custom Header feature.
 */
require get_template_directory() . '/inc/custom-header.php';

/**
 * Custom template tags for this theme.
 */
require get_template_directory() . '/inc/template-tags.php';

/**
 * Functions which enhance the theme by hooking into WordPress.
 */
require get_template_directory() . '/inc/template-functions.php';

/**
 * Customizer additions.
 */
require get_template_directory() . '/inc/customizer.php';

/**
 * Meta boxes.
 */
require get_template_directory() . '/inc/meta-boxes.php';

/**
 * Widget for showing recent post
 */
require get_template_directory() . '/inc/widgets/class-cenote-widget-recent-posts.php';

/**
 * Load Jetpack compatibility file.
 */
if ( defined( 'JETPACK__VERSION' ) ) {
	require get_template_directory() . '/inc/jetpack.php';
}

/**
 * Load WooCommerce compatibility file.
 */
if ( class_exists( 'WooCommerce' ) ) {
	require get_template_directory() . '/inc/woocommerce.php';
}

/**
 * Add Kirki customizer library file
 */
require get_template_directory() . '/inc/kirki/kirki.php';

/**
 * Add Kirki options file
 */
require get_template_directory() . '/inc/customizer/kirki-customizer.php';

/**
 * Add theme css class control file
 */
require get_template_directory() . '/inc/template-css-class.php';

/**
 * Load breadcrumb trail file if enabled.
 */
if ( true === get_theme_mod( 'cenote_breadcrumb', true ) ) {
	require get_template_directory() . '/inc/compatibility/class-breadcrumb-trail.php';
}

/**
 * Load Demo Importer Configs.
 */
if ( class_exists( 'TG_Demo_Importer' ) ) {
	require get_template_directory() . '/inc/demo-config.php';
}

/**
 * Assign the Cenote version to a variable.
 */
$cenote_theme = wp_get_theme( 'cenote' );

define( 'CENOTE_THEME_VERSION', $cenote_theme->get( 'Version' ) );

/**
 * Calling in the admin area for the new theme notice.
 */
if ( is_admin() ) {
	require get_template_directory() . '/inc/admin/class-cenote-admin.php';
	require get_template_directory() . '/inc/admin/class-cenote-notice.php';
	require get_template_directory() . '/inc/admin/class-cenote-theme-review-notice.php';
	require get_template_directory() . '/inc/admin/class-cenote-upgrade-notice.php';
	require get_template_directory() . '/inc/admin/class-cenote-dashboard.php';
	require get_template_directory() . '/inc/admin/class-cenote-welcome-notice.php';
	require get_template_directory() . '/inc/admin/class-cenote-tdi-notice.php';
}
