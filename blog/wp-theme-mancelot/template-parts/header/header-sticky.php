<?php
/**
 * Sticky header.
 *
 * @package cenote
 */

?>
	<nav id="cenote-sticky-header" class="cenote-header-sticky <?php echo esc_attr( ( is_single() ? 'cenote-header-sticky--single' : '' ) ); ?>">
		<div class="sticky-header-slide">
			<div class="cenote-reading-bar">
				<div class="tg-container tg-flex-container tg-flex-item-centered">
					<?php if ( is_single() ) : ?>
						<div class="cenote-reading-bar__title">
							<?php the_title( '<span>', '</span>', true ); ?>
						</div>
					<?php endif; ?>
				</div>
				<!-- /.tg-container -->
			</div>
			<!-- /.cenote-reading-bar -->

			<div class="cenote-sticky-main">
				<div class="tg-container tg-flex-container tg-flex-space-between tg-flex-item-centered">
					<nav class="main-navigation cenote-sticky-navigation tg-site-menu--default">
						<?php
						// Only show menu if the menu style is default.
						if ( 'tg-site-menu--default' === get_theme_mod( 'cenote_menu_style', 'tg-site-menu--default' ) ) {
							wp_nav_menu(
								array(
									'theme_location' => 'tg-menu-primary',
									'menu_id'        => 'primary-menu',
								)
							);
						}
						?>
					</nav>
					<!-- /.main-navigation cenote-sticky-navigation -->

					<?php get_template_part( 'template-parts/header/header', 'action' ); ?>

				</div>
				<!-- /.tg-container -->
			</div>
			<!-- /.cenote-header-sticky__top -->
		</div>
		<!-- /.sticky-header-slide -->
	</nav>
	<!-- /#cenote-sticky-menu.cenote-menu-sticky -->
