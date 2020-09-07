<?php
/**
 * Header to show when style is center.
 *
 * @package cenote
 */

?>
<div class="header-bottom-top">
	<div class="tg-container tg-flex-container tg-flex-space-between tg-flex-item-centered">
		<?php get_template_part( 'template-parts/header/site', 'branding' ); ?>
	</div><!-- /.tg-container -->
</div>
<!-- /.header-bottom-top -->

<div class="header-bottom-bottom">
	<div class="tg-container tg-flex-container tg-flex-space-between tg-flex-item-centered">
		<?php
			get_template_part( 'template-parts/menu/menu', 'social' );
			get_template_part( 'template-parts/menu/menu', 'primary' );
			get_template_part( 'template-parts/header/header', 'action' );
		?>
	</div><!-- /.tg-header -->
</div>
<!-- /.header-bottom-bottom -->
