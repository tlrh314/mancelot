<?php
/**
 * Displays Social Menu
 *
 * @package Cenote
 */

?>

<nav class="tg-social-menu-navigation">
	<?php
	// Get social icons.
	$social_icons = get_theme_mod( 'cenote_social_icons_lists', array(
		array(
			'social_icon' => 'tg-icon-facebook',
			'social_url'  => '#',
		),
		array(
			'social_icon' => 'tg-icon-twitter',
			'social_url'  => '#',
		),
	) );

	if ( ! empty( $social_icons ) && is_array( $social_icons ) ) :
		?>

		<ul class="tg-social-menu">
			<?php
			// Loop through each of the social links.
			foreach ( $social_icons as $social_icon ) {
				if ( ! empty( $social_icon['social_url'] ) ) :
					?>

					<li class="social-link">
						<a href="<?php echo esc_url( $social_icon['social_url'] ); ?>">
							<i class="<?php echo esc_attr( $social_icon['social_icon'] ); ?>"></i>
						</a>
					</li>

				<?php
				endif;
			}
			?>
		</ul>

	<?php endif; ?>
</nav><!-- /.tg-social-menu -->
