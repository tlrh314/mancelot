<?php
/**
 * Displays recent post with thumbnail
 *
 * @package    Cenote
 * @subpackage Widgets
 * @since      1.0.0
 */

/**
 * Class to show recent post with an image
 */
class Cenote_Widget_Recent_Posts extends WP_Widget {

	/**
	 * Set up new recent post widget
	 */
	public function __construct() {
		$widget_ops = array(
			'classname'                   => 'tg_widget_recent_posts',
			'description'                 => esc_html__( 'Shows recent posts with an image', 'cenote' ),
			'customize_selective_refresh' => true,
		);
		parent::__construct( 'tg-recent-posts', esc_html__( 'TG: Recent Posts', 'cenote' ), $widget_ops );
		$this->alt_option_name = 'tg_widget_recent_posts';
	}

	/**
	 * Output the html markup
	 *
	 * @param array $args     display arguments.
	 * @param array $instance settings for the current.
	 *
	 * @return void
	 */
	public function widget( $args, $instance ) {
		if ( ! isset( $args ['widget_id'] ) ) {
			$args['widget_id'] = $this->id;
		}
		$title  = ( ! empty( $instance['title'] ) ) ? $instance['title'] : esc_html__( 'Recent Posts', 'cenote' );
		$title  = apply_filters( 'widget_title', $title, $instance, $this->id_base );
		$number = ( ! empty( $instance['number'] ) ) ? absint( $instance['number'] ) : 5;

		if ( ! $number ) {
			$number = 5;
		}
		$show_date = isset( $instance['show_date'] ) ? $instance['show_date'] : false;

		$r = new WP_Query(
			apply_filters(
				'cenote_widget_posts_args',
				array(
					'posts_per_page'      => $number,
					'no_found_rows'       => true,
					'post_status'         => 'publish',
					'ignore_sticky_posts' => true,
				),
				$instance
			)
		);
		if ( ! $r->have_posts() ) {
			return;
		}
		?>
		<?php echo $args['before_widget']; // WPCS: XSS OK. ?>
		<?php
		if ( $title ) {
			echo $args['before_title'] . $title . $args['after_title']; // WPCS: XSS OK.
		}
		?>
		<ul>
			<?php foreach ( $r->posts as $recent_post ) : ?>
				<?php
				$post_title = get_the_title( $recent_post->ID );
				$title      = ( ! empty( $post_title ) ) ? $post_title : esc_html__( '(no title)', 'cenote' );
				?>
				<li>
					<?php if ( has_post_thumbnail( $recent_post->ID ) ) : ?>
						<a class="tg-post-thumbnail tg-recent-post-thumbnail" href="<?php the_permalink( $recent_post->ID ); ?>"><?php echo get_the_post_thumbnail( $recent_post->ID, 'thumbnail' ); ?></a>
					<?php endif; ?>
					<div class="tg-post-info tg-recent-post-info">
						<a href="<?php the_permalink( $recent_post->ID ); ?>"><?php echo esc_html( $title ); ?></a>
						<?php if ( $show_date ) : ?>
							<span class="post-date"><?php echo get_the_date( '', $recent_post->ID ); ?></span>
						<?php endif; ?>
					</div>
				</li>
			<?php endforeach; ?>
		</ul>
		<?php
		echo $args['after_widget']; // WPCS: XSS OK.
	}

	/**
	 * Update widget settings
	 *
	 * @param array $new_instance new settings.
	 * @param array $old_instance old settings.
	 *
	 * @return array updated settings to save.
	 */
	public function update( $new_instance, $old_instance ) {
		$instance              = $old_instance;
		$instance['title']     = sanitize_text_field( $new_instance['title'] );
		$instance['number']    = (int) $new_instance['number'];
		$instance['show_date'] = isset( $new_instance['show_date'] ) ? (bool) $new_instance['show_date'] : false;

		return $instance;
	}

	/**
	 * Shows the form in the back-end.
	 *
	 * @param array $instance settings.
	 */
	public function form( $instance ) {
		$title     = isset( $instance['title'] ) ? esc_attr( $instance['title'] ) : '';
		$number    = isset( $instance['number'] ) ? absint( $instance['number'] ) : 5;
		$show_date = isset( $instance['show_date'] ) ? (bool) $instance['show_date'] : false;
		?>
		<p>
			<label for="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>"><?php esc_html_e( 'Title:', 'cenote' ); ?></label>
			<input class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'title' ) ); ?>" type="text" value="<?php echo esc_attr( $title ); ?>" />
		</p>

		<p>
			<label for="<?php echo esc_attr( $this->get_field_id( 'number' ) ); ?>"><?php esc_html_e( 'Number of posts to show:', 'cenote' ); ?></label>
			<input class="tiny-text" id="<?php echo esc_attr( $this->get_field_id( 'number' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'number' ) ); ?>" type="number" step="1" min="1" value="<?php echo esc_attr( $number ); ?>" size="3" />
		</p>

		<p>
			<input class="checkbox" type="checkbox"<?php checked( $show_date ); ?> id="<?php echo esc_attr( $this->get_field_id( 'show_date' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'show_date' ) ); ?>" />
			<label for="<?php echo esc_attr( $this->get_field_id( 'show_date' ) ); ?>"><?php esc_html_e( 'Display post date?', 'cenote' ); ?></label>
		</p>
		<?php
	}
}

register_widget( 'Cenote_Widget_Recent_Posts' );
